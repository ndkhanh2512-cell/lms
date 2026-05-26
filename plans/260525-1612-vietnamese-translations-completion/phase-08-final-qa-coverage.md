---
phase: 8
status: pending
priority: high
effort: M
blockedBy: [phase-07]
---

# Phase 8 — Final QA Click-Through + Coverage Report

## Context Links
- [plan.md](plan.md)
- [phase-06-frontend-hardcoded-audit.md](phase-06-frontend-hardcoded-audit.md)
- [phase-07-backend-python-audit.md](phase-07-backend-python-audit.md)
- [Extended brainstorm 2026-05-26](../reports/brainstormer-260526-1016-vietnamese-i18n-coverage.md)

## Overview
**Priority:** High
**Status:** Pending
Final verification phase. Manual click-through 10 priority pages × 2 modes (EN/VI), generate coverage report, document any residual EN strings (whitelist), update `docs/` với i18n status. KHÔNG dịch thêm — chỉ verify + report.

## Key Insights
- Phase 1-7 đã ship 100% scope; Phase 8 catch sót + report
- Manual QA bắt buộc — script không phát hiện được dynamic strings render runtime
- Coverage = msgid translated / total + Vue files wrapped / total + Python files wrapped / total
- Whitelist documented = intentional EN (Quiz, Badge, Webinar, Module, Cohort, Batch, API…)
- Output report dùng cho release notes

## Requirements

### Functional
- QA checklist execute 10 priority pages × VI mode
- Coverage report markdown generate được từ verification script
- Update `docs/codebase-summary.md` với i18n status
- Update `docs/code-standards.md` thêm i18n rule

### Non-functional
- Report < 800 LOC
- Reproducible: anyone chạy `python scripts/check-vi-coverage.py --report` ra cùng output

## Workflow

### Step 1 — Extend coverage script
Update `scripts/check-vi-coverage.py`:
- `--report` mode: generate markdown coverage report
- Output: `plans/.../reports/i18n-coverage-final.md`
- Sections:
  - vi.po stats: total msgids, translated, empty, % coverage
  - Frontend stats: total Vue files, % files using `__()`, candidate hardcoded count
  - Backend stats: total Python files, % files có `frappe._()` usage
  - Whitelist: intentional EN strings (manual curated list)
  - Top 20 untranslated msgid by usage frequency

### Step 2 — QA checklist execute
Run manual click-through trên local `bench start` (hoặc staging):

**Priority Pages (10):**
1. ✅ `/login` — login form, signup link, forgot password
2. ✅ `/courses` — listing, filter, search, sort
3. ✅ `/courses/{name}` — course detail, enroll button, lesson list
4. ✅ `/courses/{name}/learn/{lesson}` — lesson viewer (text + video + quiz + assignment types)
5. ✅ `/profile/{username}` — profile page, edit button
6. ✅ `/notifications` — notification list, mark read
7. ✅ Sidebar — all nav links, user dropdown, language toggle
8. ✅ `/quizzes/{id}` — quiz interface, submit, results
9. ✅ `/batches/{name}` — batch page, enrollment, schedule
10. ✅ Admin: `/courses/new`, `/lessons/new` — admin edit screens

**Per page:**
- Switch sang VI → screenshot lưu vào `plans/.../qa-screenshots/{page}-vi.png`
- Note residual EN strings vào checklist
- Verify no rendering break (layout, overflow, truncation)

### Step 3 — Trigger error paths
Test 5 error scenarios:
1. Login wrong password
2. Submit empty quiz answer
3. Upload oversized assignment file
4. Access unauthorized course
5. Network error fetch

Verify error messages hiển thị VI.

### Step 4 — Generate coverage report
```bash
python scripts/check-vi-coverage.py --report --output plans/260525-1612-vietnamese-translations-completion/reports/i18n-coverage-final.md
```

### Step 5 — Update docs
- `docs/codebase-summary.md`: thêm section "Internationalization" với coverage stats
- `docs/code-standards.md`: thêm rule i18n
  - All UI text MUST use `__()` (Vue) / `frappe._()` (Python)
  - Glossary at `plans/260525-1612-.../glossary.md`
  - Add new strings → run `bench update-translations lms` → AI batch dịch → review
- `docs/development-roadmap.md`: mark "Vietnamese i18n complete" milestone
- `docs/project-changelog.md`: add entry "Vietnamese translation coverage 95%+"

### Step 6 — Cross-plan archive
- Mark plan `260525-1612-vietnamese-translations-completion` status: `completed`
- Run `/ck:plan archive` để journal entry + cleanup

## Related Code Files

**Create:**
- `plans/260525-1612-vietnamese-translations-completion/reports/i18n-coverage-final.md`
- `plans/260525-1612-vietnamese-translations-completion/qa-screenshots/*.png` (10 screenshots)
- `plans/260525-1612-vietnamese-translations-completion/qa-checklist-results.md`

**Modify:**
- `scripts/check-vi-coverage.py` (add `--report` mode)
- `docs/codebase-summary.md`
- `docs/code-standards.md`
- `docs/development-roadmap.md`
- `docs/project-changelog.md`

## Todo List
- [ ] Step 1: Extend `check-vi-coverage.py` với `--report` mode
- [ ] Step 2: QA click-through 10 priority pages, capture screenshots
- [ ] Step 3: Trigger + verify 5 error paths VI display
- [ ] Step 4: Generate coverage report markdown
- [ ] Step 5: Update 4 docs files
- [ ] Step 6: Mark plan completed, run `/ck:plan archive`

## Success Criteria
- 10/10 priority pages render VI đầy đủ (residual EN = intentional whitelist only)
- 5/5 error paths hiển thị VI
- Coverage report generated, vi.po coverage ≥95%
- 4 docs files updated
- Plan marked `completed` trong frontmatter

## Risk Assessment
| Risk | Severity | Mitigation |
|------|----------|------------|
| Phát hiện EN sót khi QA → loop ngược Phase 6/7 | Medium | Document trong residual list, batch fix nhỏ trước archive |
| Screenshot ngốn disk | Low | Compress PNG, hoặc keep top 10 only |
| Docs update conflict với plan khác | Low | Sequential commit, không parallel docs edit |

## Security Considerations
- Screenshots không chứa user data thật (dùng test account)
- Coverage report không leak file paths nhạy cảm

## Next Steps
- Sau Phase 8: Cross-plan archive, journal, retrospective
- Follow-up: GitHub Action CI gate check coverage trên PR future
- Follow-up: Crowdin sync policy decide (open question #1)
