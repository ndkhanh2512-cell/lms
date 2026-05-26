"""Apply translations.json to vi.po via Babel.

Usage:
    python apply-translations.py <vi.po> <translations.json>

Rules:
- Only updates entries whose msgstr is currently empty AND not flagged 'fuzzy'.
- Skips entries whose translation contains placeholder/HTML mismatch vs msgid.
- Reports counts: applied / skipped_already_translated / skipped_placeholder_mismatch / missing_in_input.
- Preserves catalog header and ordering.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from babel.messages.pofile import read_po, write_po

PLACEHOLDER_RE = re.compile(r"\{[0-9a-zA-Z_]+\}|%\([^)]+\)s|%s|%d")
HTML_TAG_RE = re.compile(r"<[^>]+>")


def placeholders(text: str) -> list[str]:
    return sorted(PLACEHOLDER_RE.findall(text or ""))


def html_tags(text: str) -> list[str]:
    return sorted(HTML_TAG_RE.findall(text or ""))


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    po_path = Path(sys.argv[1])
    tx_path = Path(sys.argv[2])

    translations = json.loads(tx_path.read_text(encoding="utf-8"))

    with po_path.open("rb") as fh:
        catalog = read_po(fh)

    applied = 0
    already = 0
    mismatch: list[str] = []
    missing: list[str] = []

    for msg in catalog:
        if not msg.id:
            continue
        msgid = msg.id[0] if isinstance(msg.id, tuple) else msg.id
        if msgid not in translations:
            continue
        if msg.string and (msg.string if isinstance(msg.string, str) else msg.string[0]):
            already += 1
            continue
        if "fuzzy" in msg.flags:
            continue
        new_value = translations[msgid]
        # Plural handling
        if isinstance(msg.id, tuple) and isinstance(new_value, list):
            new_str = tuple(new_value)
        else:
            new_str = new_value if isinstance(new_value, str) else new_value[0]

        # Placeholder + HTML safety check
        target = new_str if isinstance(new_str, str) else new_str[0]
        if placeholders(target) != placeholders(msgid):
            mismatch.append(msgid)
            continue
        if html_tags(target) != html_tags(msgid):
            mismatch.append(msgid)
            continue

        msg.string = new_str
        applied += 1

    seen = {msg.id[0] if isinstance(msg.id, tuple) else msg.id for msg in catalog if msg.id}
    for k in translations:
        if k not in seen:
            missing.append(k)

    with po_path.open("wb") as fh:
        write_po(fh, catalog, sort_output=False, sort_by_file=False, width=0)

    print(f"applied={applied}")
    print(f"already_translated={already}")
    print(f"placeholder_or_html_mismatch={len(mismatch)}")
    if mismatch:
        for m in mismatch[:10]:
            print(f"  MISMATCH: {m[:80]}")
    print(f"missing_in_po={len(missing)}")
    if missing:
        for m in missing[:10]:
            print(f"  MISSING: {m[:80]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
