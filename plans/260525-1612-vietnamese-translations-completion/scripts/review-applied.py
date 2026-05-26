"""Manual review helper — surface entries needing eyeball check.

Usage:
    python review-applied.py <vi.po> <translations.json>

Output sections:
- LONG: msgstr where len(msgid) > 100
- CTX: entries with msgctxt (independent context, may need different VI per context)
- HTML: entries containing HTML tags
- NEWLINE: entries containing literal \n
- 20 random sampled for tone spot-check
"""
from __future__ import annotations

import json
import random
import sys
from pathlib import Path

from babel.messages.pofile import read_po


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    po_path = Path(sys.argv[1])
    tx_path = Path(sys.argv[2])
    targets = set(json.loads(tx_path.read_text(encoding="utf-8")).keys())

    with po_path.open("rb") as fh:
        catalog = read_po(fh)

    long_, ctx, html, newline = [], [], [], []
    all_in_scope = []
    for msg in catalog:
        mid = msg.id[0] if isinstance(msg.id, tuple) else msg.id
        if not mid or mid not in targets:
            continue
        mstr = msg.string if isinstance(msg.string, str) else (msg.string[0] if msg.string else "")
        rec = (mid, mstr)
        all_in_scope.append(rec)
        if len(mid) > 100:
            long_.append(rec)
        if msg.context:
            ctx.append(rec)
        if "<" in mid and ">" in mid:
            html.append(rec)
        if "\\n" in mid or "\n" in mid:
            newline.append(rec)

    def show(title: str, items: list[tuple[str, str]], limit: int = 99) -> None:
        print(f"\n== {title} ({len(items)}) ==")
        for mid, mstr in items[:limit]:
            print(f"  EN: {mid[:120]}")
            print(f"  VI: {mstr[:120]}")
            print()

    show("LONG (>100 chars)", long_)
    show("MSGCTXT", ctx)
    show("HTML", html)
    show("NEWLINE", newline)

    random.seed(42)
    sample = random.sample(all_in_scope, min(20, len(all_in_scope)))
    show("RANDOM 20 SPOT-CHECK", sample)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
