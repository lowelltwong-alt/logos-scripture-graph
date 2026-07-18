#!/usr/bin/env python3
"""CLI for governed IIIF manuscript acquisition."""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.acquisition.iiif_acquisition_core import AcquisitionRunner, disk_free_bytes, load_config
from scripts.acquisition.rights_catalog import (
    ensure_collision_report,
    mirror_compact_manifests,
    write_codex_catalog,
    write_permission_review_queue,
    write_phase_completion_report,
    write_rights_ledger,
    write_storage_ledger,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Governed IIIF acquisition runner")
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--mode", required=True, choices=["inventory", "acquire", "verify", "status", "resume", "init-catalog", "finalize-phases"])
    parser.add_argument("--rights-ledger", required=True)
    parser.add_argument("--nas-root", required=True)
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    cfg = load_config(Path(args.config), args.task_id, Path(args.nas_root))
    rights_path = Path(args.rights_ledger)

    if args.mode == "init-catalog":
        free_before = disk_free_bytes(cfg.nas_root)
        write_rights_ledger(rights_path)
        write_codex_catalog(cfg.catalog_root / "codex_catalog.jsonl")
        write_storage_ledger(cfg.catalog_root / "storage_ledger.json", cfg.nas_root, free_before)
        write_permission_review_queue(cfg.catalog_root)
        ensure_collision_report(cfg.catalog_root)
        mirror = ROOT / ".ai/control/T479_rights_ledger_mirror.yaml"
        mirror.write_text(rights_path.read_text(encoding="utf-8"), encoding="utf-8")
        print("init-catalog complete")
        return 0

    runner = AcquisitionRunner(cfg, rights_path)
    if args.mode == "finalize-phases":
        free_before = disk_free_bytes(cfg.nas_root)
        write_rights_ledger(rights_path)
        write_codex_catalog(cfg.catalog_root / "codex_catalog.jsonl")
        write_permission_review_queue(cfg.catalog_root)
        ensure_collision_report(cfg.catalog_root)
        status = runner.status()
        verify = runner.verify()
        write_phase_completion_report(cfg.catalog_root, {**status, **verify})
        mirror_compact_manifests(cfg.catalog_root, cfg.nas_root)
        write_storage_ledger(
            cfg.catalog_root / "storage_ledger.json",
            cfg.nas_root,
            free_before,
            disk_free_bytes(cfg.nas_root),
        )
        mirror = ROOT / ".ai/control/T479_rights_ledger_mirror.yaml"
        mirror.write_text(rights_path.read_text(encoding="utf-8"), encoding="utf-8")
        import json

        print(json.dumps(verify, indent=2))
        return 0

    if args.mode == "inventory":
        result = runner.inventory()
    elif args.mode in ("acquire", "resume"):
        result = runner.acquire() if args.mode == "acquire" else runner.resume()
    elif args.mode == "status":
        result = runner.status()
    elif args.mode == "verify":
        result = runner.verify()
        ledger = cfg.catalog_root / "storage_ledger.json"
        if ledger.exists():
            import yaml

            data = yaml.safe_load(ledger.read_text(encoding="utf-8"))
            data["free_bytes_after"] = disk_free_bytes(cfg.nas_root)
            ledger.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    else:
        raise SystemExit(f"unsupported mode {args.mode}")

    import json

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
