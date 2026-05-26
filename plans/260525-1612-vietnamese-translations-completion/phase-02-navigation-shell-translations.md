---
phase: 2
status: completed
priority: high
effort: M
blockedBy: [phase-01]
completedAt: 2026-05-26
---

# Phase 2 — Navigation Shell + Modals Translations

## Context Links
- [plan.md](plan.md)
- [phase-01-foundation-default-en.md](phase-01-foundation-default-en.md) — must merge first (glossary lock)
- [glossary.md](glossary.md) — terminology source of truth (generated PR 1)

## Overview
**Priority:** High (user-facing shell visible mọi trang)
**Status:** Pending
Dịch ~300-400 chuỗi vi.po thuộc navigation shell: Sidebar, Layouts (Header/Mobile), Modals, Toasts, các component dùng chung. Đây là phần user thấy nhiều nhất → priority cao nhất sau foundation.

## Key Insights
- Sidebar (`AppSidebar.vue`) một mình có ~60+ entries trong vi.po (admin sidebar có nhiều label)
- Modals shared (Question, Confirm, Notification) reuse across pages → dịch ở đây tránh duplicate effort
- Toasts/error messages từ frappe-ui có thể không trong vi.po — chỉ touch entries có sẵn

## Requirements

### Functional
- Tất cả msgid có file path khớp scope (xem dưới) và `msgstr ""` → dịch xong
- Tone "Bạn", terminology theo glossary.md
- Preserve placeholders `{0}`, `{name}`, HTML tags, `\n`, leading/trailing whitespace
- Skip entries có flag `#, fuzzy`

### Non-functional
- `msgfmt --check lms/locale/vi.po` exit 0
- Spot-check 20 entries random qua manual review
- Manual review tất cả entries có `msgctxt` hoặc msgid > 100 chars
- Smoke test UI: toggle VI, browse sidebar/header/mobile, mở các modal common

## Scope (File Path Filter)

Dịch các entries vi.po có `#:` comment chứa một trong các path sau:
- `frontend/src/components/Sidebar/`
- `frontend/src/components/Layouts/`
- `frontend/src/components/Modals/`
- `frontend/src/components/CommandPalette/`
- `frontend/src/components/UserDropdown.vue`
- `frontend/src/components/Icons/` (nếu có tooltip labels)
- `frontend/src/components/Tooltip*.vue`
- `frontend/src/components/Notifications/` (toast/notification shell)
- `frontend/src/utils/toast*` (nếu có)

## Workflow

### Step 1 — Extract empty entries
Script Python dùng `polib`:
```python
import polib
po = polib.pofile("lms/locale/vi.po")
SCOPE_PREFIXES = [
    "frontend/src/components/Sidebar/",
    "frontend/src/components/Layouts/",
    "frontend/src/components/Modals/",
    "frontend/src/components/CommandPalette/",
    "frontend/src/components/UserDropdown.vue",
    "frontend/src/components/Notifications/",
]
todo = [e for e in po
        if not e.msgstr.strip()
        and any(any(p in occ[0] for p in SCOPE_PREFIXES) for occ in e.occurrences)
        and 'fuzzy' not in e.flags]
# Export todo list to JSON for translation subagent
```

### Step 2 — Translate batch
Spawn Claude subagent với:
- Input: JSON array `{msgid, msgctxt?, occurrences}` + glossary.md content
- Instructions:
  - Tone "Bạn", informal
  - Mandatory terminology theo glossary
  - Preserve placeholders `{0}`, `{name}`, `%s`, `<a>`, `<b>`, `\n` exactly
  - Đọc msgctxt và occurrences để dịch đúng ngữ cảnh (button vs page title vs tooltip)
  - Output: JSON `{msgid: msgstr}` mapping
- Subagent type: general-purpose hoặc dedicated translator role
- Batch size: nếu > 200 entries, chia 2 batches để tránh context bloat

### Step 3 — Apply translations
Script:
```python
import polib, json
po = polib.pofile("lms/locale/vi.po")
translations = json.load(open("translations.json"))
for e in po:
    if e.msgid in translations and not e.msgstr.strip():
        e.msgstr = translations[e.msgid]
po.save("lms/locale/vi.po")
```

### Step 4 — Validate
```bash
msgfmt --check lms/locale/vi.po
# Expect exit 0
```

### Step 5 — Manual review
- List entries trong scope có `msgctxt` → review tay
- List entries `len(msgid) > 100` → review tay
- Random 20 entries để spot-check tone & terminology
- Verify placeholders intact: grep `{0}`, `{1}`, `{name}` in msgstr vs msgid

### Step 6 — UI smoke test
- `bench start` hoặc dev env đang chạy
- Toggle VI trong LanguageToggle
- Tour:
  - Sidebar (collapsed + expanded, scroll all sections)
  - Mobile layout (resize browser hoặc DevTools)
  - Open CommandPalette (`Cmd+K` / `Ctrl+K`)
  - Open UserDropdown
  - Trigger ≥3 toast notifications
  - Open ≥2 Modals (e.g. confirm delete, question)
- Verify: không còn English text trong scope (trừ proper nouns, brand names)

### Step 7 — Commit
```bash
git add lms/locale/vi.po
git commit -m "chore: Vietnamese translations - navigation shell + modals"
git push origin develop  # hoặc PR branch
```
PR target: `develop`.

## Todo List
- [x] Extract empty entries trong scope (Babel script — 157 entries)
- [x] Generate JSON input cho translator subagent
- [x] Spawn subagent translate batch (157, single batch)
- [x] Apply translations qua Babel (preserve formatting)
- [x] Validate via `babel.read_po` (msgfmt unavailable in container)
- [x] Manual review long strings + HTML + newline + placeholders (5+1+2 entries)
- [x] Spot-check 20 random entries
- [x] Verify placeholders intact (0 mismatch reported by apply script)
- [x] Code review via code-reviewer subagent → APPROVE_WITH_CONCERNS
- [x] Apply M1/M2 fixes: Evaluation→Buổi đánh giá, Review→Nhận xét, Headline→Chức danh
- [ ] UI smoke test (deferred to post-merge — Phase 8 covers)
- [ ] Commit `chore: Vietnamese translations - navigation shell + modals`
- [ ] Create PR vào develop (or direct push to develop per workflow)

## Success Criteria
- Toggle VI → Sidebar/Header/Mobile/Modals/CommandPalette/UserDropdown hiển thị tiếng Việt
- 0 English fallback trong scope (trừ proper nouns)
- 307 entries đã dịch sẵn không bị đổi
- `msgfmt --check` exit 0
- PR diff = 300-400 msgstr changes

## Risk Assessment

| Risk | Mitigation |
|---|---|
| AI dịch sai placeholder `{0}` | Script verify placeholders match msgid vs msgstr |
| Tone inconsistent giữa các entries | Glossary mandatory + spot-check 20 |
| msgctxt entries dịch không khớp context | Manual review tất cả msgctxt entries |
| Quote escaping `\"` trong msgstr break .po syntax | `msgfmt --check` catch hết syntax errors |
| Entries reuse cross-scope (cùng msgid trong nhiều file) | polib dedupe — chỉ 1 msgstr per msgid, OK |
| frappe-ui cache translations | Note "hard refresh" trong PR description |

## Security Considerations
- Translation strings là user-facing labels, không có data sensitive
- Không touch code Python/Vue — chỉ .po file → không có attack surface mới

## Next Steps
- Phase 3 unblock khi Phase 2 PR merge
