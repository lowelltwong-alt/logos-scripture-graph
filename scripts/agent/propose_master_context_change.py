#!/usr/bin/env python3
"""AI agents propose MASTER_CONTEXT changes — never edit MASTER_CONTEXT.md directly."""
from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RECOMMENDATIONS = ROOT / ".ai" / "context" / "recommendations"


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:60] or "proposal"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent", required=True, help="Agent name proposing the change")
    parser.add_argument("--summary", required=True, help="One-line summary")
    parser.add_argument("--body", default="", help="Proposal body text")
    parser.add_argument("--body-file", default="", help="Path to proposal body markdown")
    args = parser.parse_args()

    body = args.body
    if args.body_file:
        body = Path(args.body_file).read_text(encoding="utf-8")

    if not body.strip():
        print("ERROR: provide --body or --body-file with rationale", file=sys.stderr)
        return 1

    RECOMMENDATIONS.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    filename = f"{ts}-{slugify(args.agent)}-{slugify(args.summary)}.md"
    path = RECOMMENDATIONS / filename

    content = f"""# Master Context Change Proposal

- proposed_by: {args.agent}
- proposed_at: {datetime.now(timezone.utc).replace(microsecond=0).isoformat()}
- summary: {args.summary}
- status: pending_human_review

## Proposed change

{body.strip()}

## Human action if approved

1. Review this proposal
2. Edit `.ai/control/MASTER_CONTEXT.md` manually
3. Run: `python scripts/agent/approve_master_context.py --approved-by "Your Name" --note "{args.summary}"`
4. Mark this proposal status: promoted | rejected
"""
    path.write_text(content, encoding="utf-8")
    print(path.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
