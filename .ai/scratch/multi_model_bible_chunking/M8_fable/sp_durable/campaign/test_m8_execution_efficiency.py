import copy
import json
from pathlib import Path
import tempfile
import unittest
import m8_execution_efficiency as e


class ContinuationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="m8-fixture-", dir=Path(__file__).resolve().parent)
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.inputs = {"source": "a" * 64, "checker": "b" * 64}
        self.base = {"schema": e.SCHEMA, "reviewer_id": "original-reviewer", "execution_id": "job#e1",
                     "input_identities": self.inputs, "previous": None, "completed_units": [{"id": "u1", "evidence": {"full": "source-based argument"}}],
                     "next_cursor": "u2", "pending_checks": ["final nonauthor check"], "status": "quota_blocked", "accepted": False}

    def save(self, name="one.json", data=None):
        p = self.root / name
        ref = e.save_delta(p, self.base if data is None else data)
        return p, ref

    def test_interruption_resume_preserves_full_units_and_no_acceptance(self):
        p, ref = self.save()
        d = copy.deepcopy(self.base)
        d.update(previous={k: ref[k] for k in ["file", "sha256"]}, execution_id="job#e2", completed_units=[{"id": "u2", "evidence": "opposing argument retained"}], next_cursor=None, status="ready_for_final_check")
        q, qref = self.save("two.json", d)
        r = e.load_chain(q, "original-reviewer", self.inputs, qref["sha256"])
        self.assertEqual([u["id"] for u in r["completed_units"]], ["u1", "u2"])
        self.assertEqual(r["completed_units"][0]["evidence"], self.base["completed_units"][0]["evidence"])
        self.assertFalse(r["accepted"])
        self.assertEqual(e.sha(p), ref["sha256"])
        self.assertEqual(r["pending_checks"], ["final nonauthor check"])

    def test_dependency_or_reviewer_change_invalidates_reuse(self):
        p, ref = self.save()
        self.assertEqual(e.load_chain(p, "original-reviewer", self.inputs, ref["sha256"])["delta_count"], 1)
        for who, pins in [("different-reviewer", self.inputs), ("original-reviewer", dict(self.inputs, source="c" * 64))]:
            with self.assertRaises(ValueError):
                e.load_chain(p, who, pins, ref["sha256"])

    def test_duplicate_unit_and_acceptance_rejected(self):
        _, ref = self.save()
        d = copy.deepcopy(self.base); d["previous"] = {k: ref[k] for k in ["file", "sha256"]}
        with self.assertRaises(ValueError): self.save("duplicate.json", d)
        d["previous"] = None; d["accepted"] = True
        with self.assertRaises(ValueError): self.save("accepted.json", d)

    def test_existing_output_never_overwritten(self):
        p, ref = self.save()
        with self.assertRaises(FileExistsError): self.save()
        self.assertEqual(e.sha(p), ref["sha256"])

    def test_corrupt_missing_or_outside_predecessor_rejected(self):
        for prev in [{"file": "missing.json", "sha256": "a" * 64}, {"file": "../other.json", "sha256": "a" * 64}]:
            d = copy.deepcopy(self.base); d["previous"] = prev
            with self.assertRaises((ValueError, FileNotFoundError)): self.save("bad.json", d)
        p, ref = self.save(); p.write_bytes(b'{"broken":')
        with self.assertRaises(ValueError): e.load_chain(p, "original-reviewer", self.inputs, ref["sha256"])

    def test_unknown_schema_and_duplicate_json_keys_rejected(self):
        d = copy.deepcopy(self.base); d["schema"] = "unknown"
        with self.assertRaises(ValueError): self.save("unknown.json", d)
        with self.assertRaises(ValueError): e.parse('{"id":1,"id":2}')

    def test_cold_resume_and_launch_contract_hashes(self):
        (self.root / "marathon_progress.yaml").write_text("current_book: Test\n", encoding="utf-8")
        (self.root / e.CONTRACT).write_text("owner contract", encoding="utf-8")
        p = self.root / e.WORKER; p.parent.mkdir(parents=True); p.write_text("worker contract", encoding="utf-8")
        text = e.resume_block(self.root)
        self.assertEqual(e.check_resume(self.root, text), [])
        (self.root / "marathon_progress.yaml").write_text("current_book: Other\n", encoding="utf-8")
        self.assertTrue(e.check_resume(self.root, text))
        text = e.resume_block(self.root)
        (self.root / e.CONTRACT).write_text("revised contract", encoding="utf-8")
        self.assertTrue(e.check_resume(self.root, text))
        brief = self.root / "brief.md"
        block = e.worker_block(self.root) + f"EFFICIENCY-OUT: {self.root}\n"
        brief.write_text(block, encoding="utf-8")
        self.assertEqual(e.check_launch(self.root, block, [brief]), [])
        self.assertTrue(e.check_launch(self.root, "old launch", [brief]))
        p.write_text("changed worker contract", encoding="utf-8")
        self.assertTrue(e.check_launch(self.root, block, [brief]))


if __name__ == "__main__":
    unittest.main()
