---
phase: 4
status: pending
priority: medium
effort: M
blockedBy: [phase-03]
---

# Phase 4 — Batches & Community Translations

## Context Links
- [plan.md](plan.md)
- [phase-03-learning-content-translations.md](phase-03-learning-content-translations.md)
- [glossary.md](glossary.md)

## Overview
**Priority:** Medium
**Status:** Pending
Dịch ~300 chuỗi vi.po: Batches (cohort-style training), Members, Certifications, Discussions, Notifications.

## Key Insights
- Batch = Lớp học (per glossary, đã set Phase 1)
- Discussion thread có labels reply/mention/quote — đảm bảo natural
- Notification template strings có placeholder `{0}` (user name) dày — verify placeholders sau dịch
- AdminBatchDashboard reuse một số label từ Phase 2 (đã dịch) — polib chỉ skip nếu msgstr non-empty

## Requirements

### Functional
- Tất cả msgid scope `msgstr ""` → dịch xong
- Terminology nhất quán glossary (đặc biệt Batch/Member/Cohort/Certificate)

### Non-functional
- Same as Phase 2-3 (msgfmt, manual review, smoke test)

## Scope (File Path Filter)

- `frontend/src/pages/Batches/`
- `frontend/src/pages/BatchDetail*`
- `frontend/src/components/Batch*`
- `frontend/src/pages/Members/`
- `frontend/src/components/Member*`
- `frontend/src/pages/Cohort*` (nếu có)
- `frontend/src/pages/Certification*`
- `frontend/src/components/Certificate*`
- `frontend/src/pages/Discussions/`
- `frontend/src/components/Discussion*`
- `frontend/src/pages/Notifications/`
- `frontend/src/components/Notifications/` (đã touch Phase 2 cho shell, đây là page-level)
- `frontend/src/components/CertifiedMembers*`

## Workflow
Same as Phase 2-3:
1. polib extract scope filter
2. Translate qua subagent
3. Apply + msgfmt validate
4. Manual review msgctxt + long
5. UI smoke test
6. Commit `chore: Vietnamese translations - batches & community`

## Smoke Test Checklist
- Batches list page
- Batch detail (member view + admin view)
- AdminBatchDashboard
- Add member to batch flow
- Certification page → list + detail
- Discussion thread → create, reply, react
- Notifications drawer/page → list, mark read
- CertifiedMembers list

## Todo List
- [ ] Extract empty entries scope filter
- [ ] Translate batch qua subagent
- [ ] Apply + msgfmt --check
- [ ] Manual review msgctxt + long strings
- [ ] Smoke test (checklist trên)
- [ ] Commit + PR

## Success Criteria
- Toggle VI → tất cả trang Batches/Members/Discussions/Notifications/Certifications hiển thị tiếng Việt
- Notification placeholders `{0}` etc preserved
- Diff = ~300 msgstr changes
- `msgfmt --check` exit 0

## Risk Assessment

| Risk | Mitigation |
|---|---|
| Notification template placeholders complex | Script verify `{N}` count match msgid/msgstr |
| Batch vs Course confusion in shared strings | Glossary clear: Batch=Lớp học, Course=Khóa học |
| Member email templates trùng với Phase 5 | Phase 4 chỉ frontend; email templates trong Phase 5 |
| Discussion markdown content dịch sai escape | Spot-check HTML/markdown entries |

## Security Considerations
- N/A (chỉ .po changes)

## Next Steps
- Phase 5 unblock khi Phase 4 PR merge
