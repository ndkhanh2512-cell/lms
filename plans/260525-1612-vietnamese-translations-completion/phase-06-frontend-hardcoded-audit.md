---
phase: 6
status: pending
priority: high
effort: L
blockedBy: [phase-05]
---

# Phase 6 — Frontend Hardcoded Strings Audit + Wrap

## Context Links
- [plan.md](plan.md)
- [phase-05-settings-doctype-emails-translations.md](phase-05-settings-doctype-emails-translations.md)
- [glossary.md](glossary.md)
- [Extended brainstorm 2026-05-26](../reports/brainstormer-260526-1016-vietnamese-i18n-coverage.md)

## Overview
**Priority:** High
**Status:** Pending
Audit toàn bộ 182 Vue files trong `frontend/src/`, wrap hardcoded English strings bằng `__()`, regen `vi.po`, dịch các msgid mới phát sinh. Phase này phụ thuộc Phase 1-5 đã ship vi.po stable.

## Key Insights
- Pre-audit baseline: 159/182 files dùng `__()`, 23 files KHÔNG dùng — start audit từ 23 files này (low-hanging fruit)
- 159 files đã dùng `__()` vẫn có thể có hardcoded EN strings rải rác (chỉ wrap một phần)
- Frappe-ui components (Button, Dialog, etc.) auto-translate label prop → không cần wrap thủ công nếu pass string trực tiếp vào prop
- Vue template syntax: `{{ __("text") }}` cho text; `:label="__('text')"` cho props; `:title="__('text')"` cho attributes
- Script setup: import `__` không cần — đã global qua `window.__` (xem `translation.js`)
- v-html / dynamic content (markdown, server response) KHÔNG wrap (data, không phải UI label)

## Requirements

### Functional
- Mọi UI-facing string trong template/script là EN literal → wrap `__()`
- `bench update-translations lms` regen vi.po có msgid mới
- AI batch dịch msgid mới theo glossary
- Verification script confirm 0 hardcoded EN trong UI-facing positions

### Non-functional
- Diff < 1500 lines per sub-PR (split theo folder nếu cần)
- Không break existing translations (307 baseline + Phase 1-5 deltas)
- Build vẫn pass: `cd frontend && yarn build` exit 0

## Scope (Priority Order)

Audit theo thứ tự (mỗi nhóm = 1 sub-PR nếu diff quá lớn):

1. **23 files chưa dùng `__()`** (catch-all baseline)
2. **Auth flow** — `frontend/src/pages/Login*.vue`, `Signup*.vue`, `ForgotPassword*.vue`
3. **Sidebar + Header + Mobile layout** — `frontend/src/components/Sidebar/*`, `Layouts/*`, `Header*`
4. **Courses listing + detail** — `frontend/src/pages/Course*.vue`, `Courses*.vue`
5. **Lesson viewer** — `frontend/src/pages/Lesson*.vue`, `components/Lesson*`
6. **Profile + Settings** — `frontend/src/pages/Profile/*`, `pages/Settings/*`
7. **Notifications + Toasts** — `frontend/src/components/Notification*`, toast usage
8. **Quizzes + Assignments + Certificates** — `frontend/src/pages/Quiz*`, `Assignment*`, `Certificate*`
9. **Batches + Programs** — `frontend/src/pages/Batch*`, `Program*`
10. **Admin/edit screens** — `frontend/src/pages/**Edit*.vue`, `Admin*`

## Workflow

### Step 1 — Build verification script first
Create `scripts/check-vi-coverage.py`:
- Argparse: `--check-hardcoded` mode scan Vue files for unwrapped EN strings
- Heuristic: regex `>[A-Z][a-z]+( [A-Z]?[a-z]+)*<` in templates not inside `__()` or `{{ }}` expressions
- Output: list of `file:line` candidates + total count
- Exit 1 if hardcoded found (CI gate)

### Step 2 — Audit nhóm 1 (23 files no `__()`)
```bash
grep -L "__(" frontend/src/**/*.vue  # list files
```
- Đọc từng file, identify UI-facing strings (button labels, headings, placeholders, tooltips, error messages)
- Wrap với `__()` — preserve placeholders nếu có
- Lưu ý: literal EN strings trong constants/enums KHÔNG wrap (data, không phải UI)

### Step 3 — Audit nhóm 2-10 (priority pages)
Per group:
- Run `python scripts/check-vi-coverage.py --check-hardcoded --path frontend/src/pages/Login*.vue` để locate candidates
- Manual review từng candidate (avoid false positives như URL strings, asset paths, debug logs)
- Wrap legit UI strings với `__()`

### Step 4 — Regen vi.po
```bash
bench update-translations lms
git checkout lms/locale/{ar,bs,cs,da,de,eo,es,fa,fr,hi,hr,hu,id,it,my,nb,nl,pl,pt,pt_BR,ru,sl,sr,sr_CS,sv,ta,th,tr,zh}.po
git diff lms/locale/vi.po  # confirm chỉ thêm msgid mới, không xóa
```

### Step 5 — AI batch dịch deltas
- Extract empty msgid mới (sau diff với main.pot pre-Phase 6)
- AI prompt: reuse system prompt Phase 2-5 (glossary + formal tone)
- Apply translations vào vi.po
- `msgfmt --check lms/locale/vi.po` exit 0

### Step 6 — Verify
- `python scripts/check-vi-coverage.py --check-hardcoded` exit 0 hoặc accepted whitelist
- `cd frontend && yarn build` exit 0
- Smoke test: switch VI → spot-check Auth flow + Course listing render correctly

## Related Code Files

**Create:**
- `scripts/check-vi-coverage.py`

**Modify (estimated):**
- 23 Vue files chưa dùng `__()`
- ~30-50 Vue files có hardcoded EN strings rải rác
- `lms/locale/vi.po` (deltas)

## Todo List
- [ ] Step 1: Build `scripts/check-vi-coverage.py` with `--check-hardcoded` mode
- [ ] Step 2: Audit 23 files chưa dùng `__()`, wrap UI strings
- [ ] Step 3: Audit priority group 2 (Auth flow)
- [ ] Step 4: Audit priority group 3 (Sidebar/Header/Mobile)
- [ ] Step 5: Audit priority group 4 (Courses)
- [ ] Step 6: Audit priority group 5 (Lesson viewer)
- [ ] Step 7: Audit priority group 6 (Profile/Settings)
- [ ] Step 8: Audit priority group 7 (Notifications/Toasts)
- [ ] Step 9: Audit priority group 8 (Quiz/Assignment/Certificate)
- [ ] Step 10: Audit priority group 9 (Batches/Programs)
- [ ] Step 11: Audit priority group 10 (Admin/edit screens)
- [ ] Step 12: Regen vi.po + revert 29 non-vi .po files
- [ ] Step 13: AI batch dịch all delta msgids
- [ ] Step 14: `msgfmt --check` + `yarn build` pass
- [ ] Step 15: Smoke test toggle EN/VI trên 3 page

## Success Criteria
- `scripts/check-vi-coverage.py --check-hardcoded` exit 0 (hoặc whitelist documented)
- vi.po có ≥95% non-empty msgstr (target 100% trừ intentional EN terms)
- Build pass, smoke test VI mode render đúng cho 3 page
- Glossary updated nếu có term mới phát sinh

## Risk Assessment
| Risk | Severity | Mitigation |
|------|----------|------------|
| False positives (wrap data strings) | Medium | Manual review từng candidate, không trust 100% regex |
| Sai placeholder `{0}` count khi wrap | High | Verification script check placeholder count match |
| Diff quá lớn merge khó | Medium | Split sub-PR theo group; mỗi sub-PR < 1500 lines |
| Frappe-ui component double-translate | Low | Test render — frappe-ui không translate lại nếu đã `__()` |

## Security Considerations
- Không wrap strings có user data (XSS risk khi pass qua translation lookup)
- Không wrap admin-only debug strings (lộ implementation detail)

## Next Steps
- Phase 7: Backend Python `frappe._()` audit
- Update `docs/code-standards.md` thêm i18n rule "All UI text must use `__()` / `frappe._()`"
