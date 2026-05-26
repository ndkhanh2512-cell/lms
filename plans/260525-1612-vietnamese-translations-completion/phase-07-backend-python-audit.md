---
phase: 7
status: pending
priority: medium
effort: M
blockedBy: [phase-06]
---

# Phase 7 — Backend Python `frappe._()` Audit + Wrap

## Context Links
- [plan.md](plan.md)
- [phase-06-frontend-hardcoded-audit.md](phase-06-frontend-hardcoded-audit.md)
- [glossary.md](glossary.md)
- [Extended brainstorm 2026-05-26](../reports/brainstormer-260526-1016-vietnamese-i18n-coverage.md)

## Overview
**Priority:** Medium
**Status:** Pending
Audit backend Python files trong `lms/**/*.py`, wrap UI-facing strings (error messages, validation, notifications, toast titles, success messages) với `frappe._()`. Phase 5 đã cover DocType JSON labels + email templates → Phase 7 chỉ focus Python source code.

## Key Insights
- Frappe convention: `frappe._("message")` cho user-facing; `frappe.throw(_("error"))` cho exceptions; `frappe.msgprint(_("info"))` cho notifications
- `_` thường import ở top: `from frappe import _` → check imports trước khi wrap
- Logger messages, debug print, internal API responses → KHÔNG wrap (không phải UI)
- Webhook payloads, JSON keys, doctype field names → KHÔNG wrap (data structure)
- Email subject + body Jinja đã handle Phase 5 — không touch
- Backend `frappe.throw()` messages hiện ra cho user qua frappe-ui toast → MUST wrap

## Requirements

### Functional
- Mọi user-facing Python string wrap `frappe._()`
- `bench update-translations lms` regen vi.po với msgid mới
- AI batch dịch deltas
- Smoke test: trigger 3 known error paths → verify hiển thị VI

### Non-functional
- Diff < 1000 lines per sub-PR
- Test suite pass: `bench --site <site> run-tests --app lms`
- Build pass

## Scope (File Path Filter)

- `lms/lms/api.py` (API responses, validation errors)
- `lms/lms/doctype/**/*.py` (DocType controllers — validate, on_submit, etc.)
- `lms/lms/utils.py` (utility functions với user-facing errors)
- `lms/lms/user.py` (auth-related messages)
- `lms/lms/course_import_export.py` (import errors)
- `lms/job/doctype/**/*.py` (job module controllers)
- `lms/overrides/*.py` (Frappe overrides nếu có user-facing strings)
- `lms/hooks.py` — KHÔNG wrap (config, không phải UI)
- `lms/patches/**/*.py` — KHÔNG wrap (one-time migrations)

## Workflow

### Step 1 — Locate candidates
```bash
# Strings trong frappe.throw / msgprint / set_value chưa wrap
grep -rn 'frappe.throw("' lms --include="*.py" | grep -v '_("'
grep -rn 'frappe.msgprint("' lms --include="*.py" | grep -v '_("'
grep -rn 'frappe.publish_realtime' lms --include="*.py" | grep -v '_("'
# Return strings chưa wrap
grep -rn 'return "' lms --include="*.py" | grep -E '"[A-Z][a-z]'
```
Generate candidate list saved to `plans/.../phase-07-candidates.txt`.

### Step 2 — Manual review candidate list
- Distinguish UI-facing vs internal
- UI-facing: error messages, toast titles, success messages, validation errors
- Internal: log messages, debug prints, raw JSON keys, doctype field names

### Step 3 — Wrap candidates
- Add `from frappe import _` nếu thiếu import
- Wrap: `frappe.throw("Course not found")` → `frappe.throw(_("Course not found"))`
- Preserve format placeholders: `_("User {0} not found").format(name)`
- Multi-line strings: use parens `_("Long ""multi-line ""text")` hoặc concat

### Step 4 — Regen vi.po
```bash
bench update-translations lms
git checkout lms/locale/{ar,bs,...,zh}.po  # 29 files
```

### Step 5 — AI batch dịch deltas
- Extract delta empty msgid
- Glossary + formal tone (Phase 2-5 prompt)
- Apply, `msgfmt --check` exit 0

### Step 6 — Smoke test
Trigger 3 known error paths:
1. Submit assignment without file → frappe.throw → toast VI
2. Enroll course đã enrolled → validation error VI
3. Access course chưa publish → permission error VI

## Related Code Files

**Modify (estimated):**
- ~20-30 Python files trong `lms/`
- `lms/locale/vi.po` (deltas ~50-150 msgids)

## Todo List
- [ ] Step 1: Run grep candidate locator, save to `phase-07-candidates.txt`
- [ ] Step 2: Manual review candidate list, mark UI vs internal
- [ ] Step 3: Wrap UI-facing strings + add `from frappe import _` imports
- [ ] Step 4: Regen vi.po, revert 29 non-vi .po
- [ ] Step 5: AI batch dịch deltas
- [ ] Step 6: `msgfmt --check` + run-tests pass
- [ ] Step 7: Smoke test 3 error paths trong VI mode

## Success Criteria
- 0 unwrapped UI-facing strings trong scope (grep verification)
- vi.po deltas dịch ≥95%
- Test suite pass
- 3 smoke tests hiển thị VI text

## Risk Assessment
| Risk | Severity | Mitigation |
|------|----------|------------|
| Wrap internal/log strings (noise vi.po) | Medium | Manual review, không trust grep 100% |
| Missing import `_` → NameError runtime | High | Per-file check import sau wrap |
| Format string error sau wrap | High | Test paths có format placeholder, `_("text {0}").format(x)` |
| Webhook payload bị translate (break integration) | Critical | Tuyệt đối không wrap JSON response keys/values |

## Security Considerations
- Không wrap user input echo (XSS qua translation lookup attack vector)
- Không wrap SQL error details (info leak)

## Next Steps
- Phase 8: Final QA + coverage report
