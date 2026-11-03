#!/usr/bin/env python3
"""The mechanics of a method version, shared by gen_method_vN.py from v8 on, so a later book writes data and no engine.

A gen_method_vN.py states what is book-specific: the pinned inputs, the anchors, the header, the change table and the
provenance tail. This file states what is not: every anchor occurs EXACTLY ONCE or the run fails, the older version's
bytes are never modified, every adopted text must stand in the output byte for byte, and a version already on disk
with other bytes is re-issued under a new number, never overwritten.

Not run directly.
"""
import hashlib
import sys

BANNED = ("TODO", "TBD", "FIXME", "XXX", "<fill", "LOREM")


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def once(text, anchor):
    n = text.count(anchor)
    if n != 1:
        sys.exit("FAIL: anchor occurs %d times, not once: %s" % (n, anchor[:60]))
    return text.index(anchor)


def replace_once(text, old, new):
    pos = once(text, old)
    return text[:pos] + new + text[pos + len(old):]


def at_section_end(text, next_heading, payload):
    """A section ends at the next section's heading, stepping back over the rule line that closes it, if any."""
    pos = once(text, next_heading)
    if text[:pos].endswith("\n---\n\n"):
        pos -= len("---\n\n")
    if not text[:pos].endswith("\n\n"):
        sys.exit("FAIL: the section before %s does not end on a blank line" % next_heading[:40])
    return text[:pos] + payload + "\n\n" + text[pos:]


def after_paragraph(text, anchor, payload):
    pos = once(text, anchor)
    end = text.index("\n\n", pos)
    return text[:end] + "\n\n" + payload + text[end:]


def after_line(text, anchor, payload):
    """For a list: the new item follows the line that holds the anchor, with no blank line between."""
    pos = once(text, anchor)
    end = text.index("\n", pos)
    return text[:end] + "\n" + payload + text[end:]


def carried(text, adopted):
    """Every adopted text must stand in the output as the adjudicator returned it."""
    for pid, t in adopted.items():
        if t not in text:
            sys.exit("FAIL: the adopted text of %s is not in the output byte for byte" % pid)
    hits = [b for b in BANNED if b in text]
    if hits or "\r" in text:
        sys.exit("FAIL: the output holds a banned token %s or a carriage return" % hits)


def run(build, out, argv):
    """Write out, or with --check regenerate twice and compare to the bytes on disk."""
    data = build()
    digest = hashlib.sha256(data).hexdigest()
    if "--check" in argv:
        again = hashlib.sha256(build()).hexdigest()
        on_disk = sha(out) if out.exists() else "ABSENT"
        ok = digest == again == on_disk
        print("regenerated %s, on disk %s: %s" % (digest[:16], on_disk[:16], "MATCH" if ok else "DIFFER"))
        sys.exit(0 if ok else 1)
    if out.exists() and sha(out) != digest:
        sys.exit("REFUSED: %s exists with other bytes; a method version is re-issued, never overwritten" % out.name)
    out.write_bytes(data)
    print("%s sha256 %s bytes %d" % (out.name, digest, len(data)))
