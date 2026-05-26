"""Extract empty vi.po entries within a path-scope filter using Babel.

Usage:
    python extract_scope.py <vi.po> <output.json> <prefix1> [prefix2 ...]

Emits JSON array of {msgid, msgctxt, occurrences, flags} for entries where:
- msgstr is empty (untranslated)
- 'fuzzy' not in flags
- at least one occurrence file path startswith one of the given prefixes
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from babel.messages.pofile import read_po


def main() -> int:
    if len(sys.argv) < 4:
        print(__doc__)
        return 2
    po_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])
    prefixes = tuple(sys.argv[3:])

    with po_path.open("rb") as fh:
        catalog = read_po(fh)

    out = []
    for msg in catalog:
        if msg.id == "" or not msg.id:
            continue  # header
        if msg.string:
            continue  # already translated
        if "fuzzy" in msg.flags:
            continue
        locs = [(f, ln) for f, ln in (msg.locations or [])]
        if not any(any(f.startswith(p) for p in prefixes) for f, _ in locs):
            continue
        # msg.id can be a tuple for plurals; treat both cases
        if isinstance(msg.id, tuple):
            msgid = msg.id[0]
            msgid_plural = msg.id[1]
        else:
            msgid = msg.id
            msgid_plural = None
        out.append(
            {
                "msgid": msgid,
                "msgid_plural": msgid_plural,
                "msgctxt": msg.context,
                "occurrences": [f"{f}:{ln}" for f, ln in locs],
                "flags": sorted(msg.flags),
            }
        )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"extracted={len(out)} -> {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
