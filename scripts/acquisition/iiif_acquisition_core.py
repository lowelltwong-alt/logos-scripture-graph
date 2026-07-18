#!/usr/bin/env python3
"""Provider-neutral IIIF Presentation 2 acquisition core for NAS storage."""
from __future__ import annotations

import hashlib
import json
import os
import random
import re
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import yaml

TOOL_REVISION = "iiif_acquisition_core.v1"
IMAGE_SIGNATURES = (
    (b"\xff\xd8\xff", "jpeg"),
    (b"\x00\x00\x00\x0cjP  ", "jpx"),
    (b"\x00\x00\x00\x0cJ P  ", "jp2"),
)


@dataclass
class AcquisitionConfig:
    task_id: str
    nas_root: Path
    source_id: str
    object_id: str
    manifest_url: str
    viewer_url: str
    rights_url: str
    holding_institution: str
    expected_canvas_count: int
    expected_leaf_count: int
    concurrency: int = 2
    request_delay_seconds: float = 0.5
    max_retries: int = 8
    user_agent: str = "LogosScriptureGraph-Acquisition/1.0"

    @property
    def staging_root(self) -> Path:
        return self.nas_root / "staging" / self.task_id

    @property
    def quarantine_root(self) -> Path:
        return self.nas_root / "quarantine" / self.task_id

    @property
    def catalog_root(self) -> Path:
        return self.nas_root / "manuscript-witnesses" / "catalog" / self.task_id

    @property
    def source_originals_root(self) -> Path:
        return (
            self.nas_root
            / "source-originals"
            / "manuscript-witnesses"
            / "greek_codices"
            / "codex_sinaiticus"
            / "leipzig"
            / self.object_id
        )

    @property
    def ops_manifest_root(self) -> Path:
        return Path(f"Z:/08-AI-Operations/manifests/{self.task_id}")

    @property
    def ops_handoff_root(self) -> Path:
        return Path(f"Z:/08-AI-Operations/handoffs/{self.task_id}")

    @property
    def provenance_root(self) -> Path:
        return self.nas_root / "provenance" / "logos-scripture-graph" / "codices" / self.task_id


@dataclass
class ImageResource:
    resource_id: str
    manifest_id: str
    canvas_id: str
    canvas_label: str
    annotation_id: str
    capture_type: str
    service_id: str
    direct_url: str
    format_hint: str
    width: int | None
    height: int | None
    rights_ledger_row: str


@dataclass
class ProgressState:
    run_id: str
    started_at: str
    updated_at: str
    manifest_sha256: str
    completed: dict[str, dict[str, Any]] = field(default_factory=dict)
    failed: dict[str, dict[str, Any]] = field(default_factory=dict)
    skipped_identical: dict[str, dict[str, Any]] = field(default_factory=dict)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def ensure_dirs(*paths: Path) -> None:
    for p in paths:
        p.mkdir(parents=True, exist_ok=True)


def append_jsonl(path: Path, row: dict[str, Any]) -> None:
    ensure_dirs(path.parent)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def write_json(path: Path, data: Any) -> None:
    ensure_dirs(path.parent)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must be a YAML mapping")
    return data


def load_config(config_path: Path, task_id: str, nas_root: Path) -> AcquisitionConfig:
    raw = load_yaml(config_path)
    return AcquisitionConfig(
        task_id=task_id,
        nas_root=Path(nas_root),
        source_id=str(raw["source_id"]),
        object_id=str(raw["object_id"]),
        manifest_url=str(raw["manifest_url"]),
        viewer_url=str(raw["viewer_url"]),
        rights_url=str(raw["rights_url"]),
        holding_institution=str(raw["holding_institution"]),
        expected_canvas_count=int(raw["expected_canvas_count"]),
        expected_leaf_count=int(raw["expected_leaf_count"]),
        concurrency=int(raw.get("concurrency", 2)),
        request_delay_seconds=float(raw.get("request_delay_seconds", 0.5)),
        max_retries=int(raw.get("max_retries", 8)),
        user_agent=str(raw.get("user_agent", "LogosScriptureGraph-Acquisition/1.0")),
    )


def disk_free_bytes(path: Path) -> int:
    try:
        usage = os.statvfs(path) if hasattr(os, "statvfs") else None
    except OSError:
        usage = None
    if usage is not None:
        return int(usage.f_bavail * usage.f_frsize)
    import shutil

    return int(shutil.disk_usage(str(path)).free)


def _label_value(label: Any) -> str:
    if isinstance(label, str):
        return label
    if isinstance(label, list):
        for item in label:
            if isinstance(item, dict):
                lang = item.get("@language", "")
                if lang == "en" and "@value" in item:
                    return str(item["@value"])
        for item in label:
            if isinstance(item, dict) and "@value" in item:
                return str(item["@value"])
    return str(label)


def _capture_type_from_label(label: Any) -> str:
    text = _label_value(label).lower()
    if "raking" in text or "streiflicht" in text:
        return "raking_light"
    if "repro" in text:
        return "reproduction"
    return "image"


def _expand_choice_resource(
    resource: dict[str, Any],
    *,
    manifest_id: str,
    canvas_id: str,
    canvas_label: str,
    annotation_id: str,
    rights_row: str,
) -> list[ImageResource]:
    out: list[ImageResource] = []
    if resource.get("@type") == "oa:Choice":
        default = resource.get("default")
        if isinstance(default, dict):
            out.extend(
                _image_resource_from_dict(
                    default,
                    manifest_id=manifest_id,
                    canvas_id=canvas_id,
                    canvas_label=canvas_label,
                    annotation_id=annotation_id,
                    rights_row=rights_row,
                )
            )
        for item in resource.get("item", []) or []:
            if isinstance(item, dict):
                out.extend(
                    _image_resource_from_dict(
                        item,
                        manifest_id=manifest_id,
                        canvas_id=canvas_id,
                        canvas_label=canvas_label,
                        annotation_id=annotation_id,
                        rights_row=rights_row,
                    )
                )
    elif isinstance(resource, dict):
        out.extend(
            _image_resource_from_dict(
                resource,
                manifest_id=manifest_id,
                canvas_id=canvas_id,
                canvas_label=canvas_label,
                annotation_id=annotation_id,
                rights_row=rights_row,
            )
        )
    return out


def _image_resource_from_dict(
    img: dict[str, Any],
    *,
    manifest_id: str,
    canvas_id: str,
    canvas_label: str,
    annotation_id: str,
    rights_row: str,
) -> list[ImageResource]:
    service = img.get("service") or {}
    service_id = str(service.get("@id", ""))
    direct_url = str(img.get("@id", ""))
    if not service_id and not direct_url:
        return []
    resource_id = _stable_resource_id(canvas_id, service_id or direct_url, _label_value(img.get("label", "")))
    return [
        ImageResource(
            resource_id=resource_id,
            manifest_id=manifest_id,
            canvas_id=canvas_id,
            canvas_label=canvas_label,
            annotation_id=annotation_id,
            capture_type=_capture_type_from_label(img.get("label", "")),
            service_id=service_id,
            direct_url=direct_url,
            format_hint=str(img.get("format", "")),
            width=int(img["width"]) if img.get("width") else None,
            height=int(img["height"]) if img.get("height") else None,
            rights_ledger_row=rights_row,
        )
    ]


def _stable_resource_id(canvas_id: str, service_or_url: str, label: str) -> str:
    tail = canvas_id.rstrip("/").split("/")[-1]
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", label.lower()).strip("_") or "image"
    svc_tail = service_or_url.rstrip("/").split("/")[-1]
    return f"canvas_{tail}_{slug}_{svc_tail}"


def parse_manifest_resources(manifest: dict[str, Any], rights_row: str) -> list[ImageResource]:
    manifest_id = str(manifest.get("@id", ""))
    resources: list[ImageResource] = []
    for sequence in manifest.get("sequences", []) or []:
        for canvas in sequence.get("canvases", []) or []:
            canvas_id = str(canvas.get("@id", ""))
            canvas_label = _label_value(canvas.get("label", ""))
            for image in canvas.get("images", []) or []:
                annotation_id = str(image.get("@id", ""))
                resource = image.get("resource")
                if isinstance(resource, dict):
                    resources.extend(
                        _expand_choice_resource(
                            resource,
                            manifest_id=manifest_id,
                            canvas_id=canvas_id,
                            canvas_label=canvas_label,
                            annotation_id=annotation_id,
                            rights_row=rights_row,
                        )
                    )
    return resources


class HttpClient:
    def __init__(self, user_agent: str, max_retries: int, delay: float) -> None:
        self.user_agent = user_agent
        self.max_retries = max_retries
        self.delay = delay
        self._lock = threading.Lock()

    def fetch(
        self,
        url: str,
        *,
        dest: Path | None = None,
        range_header: str | None = None,
        stream: bool = False,
    ) -> tuple[bytes | None, dict[str, Any]]:
        meta: dict[str, Any] = {
            "requested_url": url,
            "final_url": url,
            "http_status": None,
            "etag": None,
            "last_modified": None,
            "content_type": None,
            "content_length": None,
            "retries": 0,
        }
        last_error: Exception | None = None
        for attempt in range(self.max_retries + 1):
            if attempt:
                meta["retries"] = attempt
                sleep_s = min(60.0, (2 ** (attempt - 1)) + random.random())
                time.sleep(sleep_s)
            headers = {"User-Agent": self.user_agent}
            if range_header:
                headers["Range"] = range_header
            req = urllib.request.Request(url, headers=headers)
            try:
                with self._lock:
                    time.sleep(self.delay)
                with urllib.request.urlopen(req, timeout=180) as resp:
                    meta["http_status"] = getattr(resp, "status", None) or resp.getcode()
                    meta["final_url"] = resp.geturl()
                    meta["etag"] = resp.headers.get("ETag")
                    meta["last_modified"] = resp.headers.get("Last-Modified")
                    meta["content_type"] = resp.headers.get("Content-Type")
                    cl = resp.headers.get("Content-Length")
                    meta["content_length"] = int(cl) if cl else None
                    if dest is not None:
                        ensure_dirs(dest.parent)
                        mode = "ab" if range_header else "wb"
                        with dest.open(mode) as out:
                            while True:
                                chunk = resp.read(1024 * 1024)
                                if not chunk:
                                    break
                                out.write(chunk)
                        return None, meta
                    data = resp.read()
                    return data, meta
            except urllib.error.HTTPError as exc:
                last_error = exc
                meta["http_status"] = exc.code
                if exc.code in (429, 500, 502, 503, 504):
                    continue
                raise
            except (urllib.error.URLError, TimeoutError, OSError) as exc:
                last_error = exc
                continue
        raise RuntimeError(f"fetch failed for {url}: {last_error}")


def detect_media_signature(path: Path) -> str | None:
    with path.open("rb") as f:
        head = f.read(16)
    for sig, name in IMAGE_SIGNATURES:
        if head.startswith(sig):
            return name
    if head[:3] == b"\xff\xd8\xff":
        return "jpeg"
    return None


def extension_for_media(media: str | None, content_type: str | None, format_hint: str) -> str:
    if media == "jpeg" or (content_type and "jpeg" in content_type):
        return ".jpg"
    if media in ("jpx", "jp2") or (content_type and "jp2" in content_type):
        return ".jpx"
    if format_hint:
        if "jpeg" in format_hint:
            return ".jpg"
        if "jp2" in format_hint or "jpx" in format_hint:
            return ".jpx"
    return ".bin"


def build_download_url(resource: ImageResource, info: dict[str, Any] | None) -> str:
    if info:
        profile = str(info.get("profile") or "")
        service_id = str(info.get("@id", resource.service_id)).rstrip("/")
        if "image/3" in profile:
            return f"{service_id}/full/max/0/default.jpg"
        sizes = info.get("sizes") or []
        if sizes:
            largest = max(sizes, key=lambda s: int(s.get("width", 0)) * int(s.get("height", 0)))
            w, h = largest.get("width"), largest.get("height")
            if w and h:
                return f"{service_id}/full/{w},{h}/0/default.jpg"
        return f"{service_id}/full/full/0/default.jpg"
    if resource.service_id:
        return f"{resource.service_id.rstrip('/')}/full/full/0/default.jpg"
    return resource.direct_url


def capture_manifest(cfg: AcquisitionConfig, client: HttpClient) -> tuple[Path, str]:
    captured = cfg.staging_root / "iiif" / "manifest.captured.json"
    if captured.exists():
        data = captured.read_bytes()
        return captured, sha256_bytes(data)
    data, meta = client.fetch(cfg.manifest_url)
    assert data is not None
    ensure_dirs(captured.parent)
    captured.write_bytes(data)
    promoted = cfg.source_originals_root / "iiif" / "manifest.json"
    ensure_dirs(promoted.parent)
    if not promoted.exists():
        promoted.write_bytes(data)
    append_jsonl(
        cfg.catalog_root / "transfer_events.jsonl",
        {"event": "manifest_captured", "timestamp": utc_now(), **meta, "sha256": sha256_bytes(data)},
    )
    return captured, sha256_bytes(data)


def fetch_info_json(cfg: AcquisitionConfig, client: HttpClient, service_id: str) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    if not service_id:
        return None, {}
    url = service_id.rstrip("/") + "/info.json"
    try:
        data, meta = client.fetch(url)
        assert data is not None
        info = json.loads(data.decode("utf-8"))
        info_path = cfg.source_originals_root / "iiif" / "info" / f"{service_id.rstrip('/').split('/')[-1]}.info.json"
        ensure_dirs(info_path.parent)
        if not info_path.exists():
            info_path.write_bytes(data)
        return info, meta
    except Exception as exc:
        return None, {"requested_url": url, "error": str(exc)}


def classify_canvas_label(label: str) -> str:
    low = label.lower()
    if any(x in low for x in ("target", "color", "blank", "guard", "binding")):
        return "non_text_artifact"
    return "mixed_or_uncertain"


class AcquisitionRunner:
    def __init__(self, cfg: AcquisitionConfig, rights_ledger_path: Path) -> None:
        self.cfg = cfg
        self.rights_ledger_path = rights_ledger_path
        self.client = HttpClient(cfg.user_agent, cfg.max_retries, cfg.request_delay_seconds)
        self.progress_path = cfg.staging_root / "progress_state.json"
        self.hash_index_path = cfg.staging_root / "hash_index.json"
        self._progress_lock = threading.Lock()
        self._heartbeat_stop = threading.Event()

    def _load_rights(self) -> dict[str, Any]:
        ledger = load_yaml(self.rights_ledger_path)
        rows = ledger.get("rows") or []
        by_source = {str(r["source_id"]): r for r in rows if isinstance(r, dict)}
        return by_source.get(self.cfg.source_id, {})

    def _load_progress(self) -> ProgressState:
        if self.progress_path.exists():
            raw = json.loads(self.progress_path.read_text(encoding="utf-8"))
            return ProgressState(**raw)
        return ProgressState(run_id=f"{self.cfg.task_id}-{int(time.time())}", started_at=utc_now(), updated_at=utc_now(), manifest_sha256="")

    def _save_progress(self, state: ProgressState) -> None:
        state.updated_at = utc_now()
        write_json(self.progress_path, asdict(state))

    def _heartbeat(self, state: ProgressState, total: int) -> None:
        while not self._heartbeat_stop.wait(900):
            done = len(state.completed) + len(state.skipped_identical)
            append_jsonl(
                self.cfg.catalog_root / "task.log",
                {
                    "timestamp": utc_now(),
                    "completed": done,
                    "total": total,
                    "failed": len(state.failed),
                    "free_bytes": disk_free_bytes(self.cfg.nas_root),
                },
            )

    def inventory(self) -> dict[str, Any]:
        ensure_dirs(
            self.cfg.staging_root,
            self.cfg.catalog_root,
            self.cfg.source_originals_root / "images",
            self.cfg.source_originals_root / "iiif",
            self.cfg.ops_manifest_root,
            self.cfg.ops_handoff_root,
            self.cfg.provenance_root,
        )
        rights = self._load_rights()
        if rights.get("decision") != "acquire":
            raise RuntimeError(f"rights ledger blocks acquisition for {self.cfg.source_id}")

        captured_path, manifest_hash = capture_manifest(self.cfg, self.client)
        manifest = json.loads(captured_path.read_text(encoding="utf-8"))
        canvas_count = sum(len(s.get("canvases", []) or []) for s in manifest.get("sequences", []) or [])
        if canvas_count != self.cfg.expected_canvas_count:
            append_jsonl(
                self.cfg.catalog_root / "collision_and_failure_report.jsonl",
                {
                    "timestamp": utc_now(),
                    "kind": "manifest_drift",
                    "expected": self.cfg.expected_canvas_count,
                    "observed": canvas_count,
                },
            )
        resources = parse_manifest_resources(manifest, str(rights.get("source_id", self.cfg.source_id)))
        inventory_path = self.cfg.catalog_root / "source_inventory.jsonl"
        if inventory_path.exists():
            inventory_path.unlink()
        map_path = self.cfg.catalog_root / "canvas_resource_map.jsonl"
        if map_path.exists():
            map_path.unlink()

        services_seen: set[str] = set()
        for res in resources:
            row = asdict(res)
            append_jsonl(inventory_path, row)
            append_jsonl(
                map_path,
                {
                    "canvas_id": res.canvas_id,
                    "canvas_label": res.canvas_label,
                    "resource_id": res.resource_id,
                    "capture_type": res.capture_type,
                    "service_id": res.service_id,
                    "lane_classification": classify_canvas_label(res.canvas_label),
                },
            )
            if res.service_id and res.service_id not in services_seen:
                services_seen.add(res.service_id)
                info, _ = fetch_info_json(self.cfg, self.client, res.service_id)

        write_json(
            self.cfg.catalog_root / "manifest_capture.json",
            {
                "manifest_path": str(captured_path),
                "manifest_sha256": manifest_hash,
                "canvas_count": canvas_count,
                "resource_count": len(resources),
                "distinct_services": len(services_seen),
                "captured_at": utc_now(),
            },
        )
        return {
            "manifest_sha256": manifest_hash,
            "canvas_count": canvas_count,
            "resource_count": len(resources),
        }

    def _destination_for(self, resource: ImageResource, ext: str) -> Path:
        return self.cfg.source_originals_root / "images" / f"{resource.resource_id}{ext}"

    def _process_one(self, resource: ImageResource, state: ProgressState) -> None:
        if resource.resource_id in state.completed or resource.resource_id in state.skipped_identical:
            return
        part = self.cfg.staging_root / "images" / f"{resource.resource_id}.part"
        info, info_meta = fetch_info_json(self.cfg, self.client, resource.service_id)
        url = build_download_url(resource, info)
        _, meta = self.client.fetch(url, dest=part)
        media = detect_media_signature(part)
        if media is None:
            append_jsonl(
                self.cfg.catalog_root / "collision_and_failure_report.jsonl",
                {
                    "timestamp": utc_now(),
                    "resource_id": resource.resource_id,
                    "kind": "invalid_media_signature",
                    "url": url,
                },
            )
            part.unlink(missing_ok=True)
            with self._progress_lock:
                state.failed[resource.resource_id] = {"reason": "invalid_media_signature", "url": url}
                self._save_progress(state)
            return
        ext = extension_for_media(media, meta.get("content_type"), resource.format_hint)
        dest = self._destination_for(resource, ext)
        digest = sha256_file(part)
        if dest.exists():
            if sha256_file(dest) == digest:
                part.unlink(missing_ok=True)
                with self._progress_lock:
                    state.skipped_identical[resource.resource_id] = {
                        "local_path": str(dest),
                        "sha256": digest,
                        "result": "already_present_identical",
                    }
                    self._save_progress(state)
                append_jsonl(
                    self.cfg.catalog_root / "transfer_events.jsonl",
                    {
                        "timestamp": utc_now(),
                        "resource_id": resource.resource_id,
                        "result": "already_present_identical",
                        "sha256": digest,
                    },
                )
                return
            q = self.cfg.quarantine_root / "images" / dest.name
            ensure_dirs(q.parent)
            part.replace(q)
            append_jsonl(
                self.cfg.catalog_root / "collision_and_failure_report.jsonl",
                {
                    "timestamp": utc_now(),
                    "resource_id": resource.resource_id,
                    "kind": "destination_collision",
                    "destination": str(dest),
                    "quarantine": str(q),
                },
            )
            with self._progress_lock:
                state.failed[resource.resource_id] = {"reason": "destination_collision", "destination": str(dest)}
                self._save_progress(state)
            return
        ensure_dirs(dest.parent)
        os.replace(part, dest)
        event = {
            "timestamp": utc_now(),
            "resource_id": resource.resource_id,
            "canvas_id": resource.canvas_id,
            "capture_type": resource.capture_type,
            "requested_url": url,
            "final_url": meta.get("final_url"),
            "http_status": meta.get("http_status"),
            "content_type": meta.get("content_type"),
            "byte_count": dest.stat().st_size,
            "etag": meta.get("etag"),
            "last_modified": meta.get("last_modified"),
            "local_relative_path": str(dest.relative_to(self.cfg.nas_root)).replace("\\", "/"),
            "sha256": digest,
            "rights_ledger_row": resource.rights_ledger_row,
            "result": "acquired",
        }
        append_jsonl(self.cfg.catalog_root / "transfer_events.jsonl", event)
        with self._progress_lock:
            state.completed[resource.resource_id] = event
            self._save_progress(state)

    def acquire(self) -> dict[str, Any]:
        inv = self.inventory()
        captured_path = self.cfg.staging_root / "iiif" / "manifest.captured.json"
        manifest = json.loads(captured_path.read_text(encoding="utf-8"))
        rights = self._load_rights()
        resources = parse_manifest_resources(manifest, str(rights.get("source_id", self.cfg.source_id)))
        state = self._load_progress()
        state.manifest_sha256 = inv["manifest_sha256"]
        self._save_progress(state)
        hb = threading.Thread(target=self._heartbeat, args=(state, len(resources)), daemon=True)
        hb.start()
        pending = [
            r
            for r in resources
            if r.resource_id not in state.completed and r.resource_id not in state.skipped_identical
        ]
        with ThreadPoolExecutor(max_workers=self.cfg.concurrency) as pool:
            futures = [pool.submit(self._process_one, r, state) for r in pending]
            for fut in as_completed(futures):
                fut.result()
        self._heartbeat_stop.set()
        return self.status()

    def resume(self) -> dict[str, Any]:
        return self.acquire()

    def status(self) -> dict[str, Any]:
        state = self._load_progress()
        captured_path = self.cfg.staging_root / "iiif" / "manifest.captured.json"
        total = 0
        if captured_path.exists():
            manifest = json.loads(captured_path.read_text(encoding="utf-8"))
            rights = self._load_rights()
            total = len(parse_manifest_resources(manifest, str(rights.get("source_id", self.cfg.source_id))))
        return {
            "run_id": state.run_id,
            "manifest_sha256": state.manifest_sha256,
            "total_resources": total,
            "completed": len(state.completed),
            "skipped_identical": len(state.skipped_identical),
            "failed": len(state.failed),
            "remaining": max(0, total - len(state.completed) - len(state.skipped_identical) - len(state.failed)),
        }

    def verify(self) -> dict[str, Any]:
        sums_path = self.cfg.catalog_root / "SHA256SUMS"
        lines: list[str] = []
        for path in sorted(self.cfg.source_originals_root.rglob("*")):
            if path.is_file():
                rel = path.relative_to(self.cfg.nas_root).as_posix()
                lines.append(f"{sha256_file(path)}  {rel}")
        sums_path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
        st = self.status()
        residual = {
            "timestamp": utc_now(),
            "total_resources": st["total_resources"],
            "completed": st["completed"],
            "skipped_identical": st["skipped_identical"],
            "failed": st["failed"],
            "remaining": st["remaining"],
            "completion_state": "complete_verified" if st["remaining"] == 0 and st["failed"] == 0 else "incomplete_resumable",
        }
        write_json(self.cfg.catalog_root / "residual_report.json", residual)
        free_after = disk_free_bytes(self.cfg.nas_root)
        receipt = {
            "run_id": st.get("run_id"),
            "task_id": self.cfg.task_id,
            "tool_revision": TOOL_REVISION,
            "manifest_sha256": st.get("manifest_sha256"),
            "counts": st,
            "free_bytes_after": free_after,
            "completed_at": utc_now(),
            "completion_state": residual["completion_state"],
        }
        write_json(self.cfg.catalog_root / "acquisition_receipt.json", receipt)
        write_json(self.cfg.provenance_root / "acquisition_receipt.json", receipt)
        write_json(self.cfg.ops_manifest_root / "acquisition_receipt.json", receipt)
        return residual
