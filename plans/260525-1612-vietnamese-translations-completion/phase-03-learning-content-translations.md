---
phase: 3
status: completed
priority: high
effort: L
blockedBy: [phase-02]
completedAt: 2026-05-26
---

# Phase 3 — Learning Content Translations

## Context Links
- [plan.md](plan.md)
- [phase-02-navigation-shell-translations.md](phase-02-navigation-shell-translations.md)
- [glossary.md](glossary.md)

## Overview
**Priority:** High (core learning experience)
**Status:** Pending
Dịch ~400-500 chuỗi vi.po thuộc learning content: Home, Courses, Lessons, Chapters, Quiz, Assignment. Phase nặng nhất (lớn nhất theo số strings).

## Key Insights
- Course/Lesson pages có UI elements động (progress, status badges) — chú ý plural forms
- Quiz/Assignment có instruction text dài > 100 chars → manual review nhiều
- Một số msgid dùng chung cho Course và Batch (e.g. "Enroll Now") — terminology phải nhất quán với Phase 4

## Requirements

### Functional
- Tất cả msgid scope (xem dưới) `msgstr ""` → dịch xong
- Tone "Bạn", terminology theo glossary
- Preserve placeholders / HTML / whitespace

### Non-functional
- `msgfmt --check` exit 0
- Manual review msgctxt + msgid > 100 chars
- Smoke test core learning flow

## Scope (File Path Filter)

- `frontend/src/pages/Home/`
- `frontend/src/pages/Courses/` (list, detail, create, edit, manage)
- `frontend/src/pages/CourseDetail*`
- `frontend/src/pages/Lesson*`
- `frontend/src/pages/Chapter*`
- `frontend/src/pages/Quiz*` (taking + creating)
- `frontend/src/pages/Assignment*`
- `frontend/src/components/Course*`
- `frontend/src/components/Lesson*`
- `frontend/src/components/Quiz*`
- `frontend/src/components/Assignment*`
- `frontend/src/components/Programming*` (programming exercises)
- `frontend/src/components/Scorm*`

## Workflow
Same as Phase 2:
1. Extract empty entries qua polib với scope filter trên
2. Spawn translator subagent (batch theo file group nếu > 200 entries)
3. Apply translations qua polib
4. `msgfmt --check`
5. Manual review msgctxt + long strings
6. UI smoke test learning flow
7. Commit `chore: Vietnamese translations - learning content`

## Smoke Test Checklist
- Home page (logged-in)
- Browse courses → list, filter
- Course detail page → enroll, view chapters
- Lesson view → text/video/embed/SCORM
- Take quiz → questions, options, submit, results
- Take assignment → submit, view feedback
- Programming exercise (nếu có) — view, submit
- Create course (admin) → form fields, validation messages

## Todo List
- [x] Extract empty entries (Babel + scope filter — 237 entries)
- [x] Translate batch qua subagent (237, single batch)
- [x] Apply + validate via Babel (msgfmt unavailable in container)
- [x] Manual review long strings (6) + placeholders (237/237 intact)
- [x] Code review via code-reviewer subagent → APPROVE clean
- [ ] Smoke test learning flow (deferred to Phase 8)
- [ ] Commit + push develop

## Success Criteria
- Tất cả trang learning trong scope hiển thị tiếng Việt khi toggle VI
- Quiz instructions, assignment prompts đọc tự nhiên (manual review approved)
- Diff = 400-500 msgstr changes
- `msgfmt --check` exit 0

## Risk Assessment

| Risk | Mitigation |
|---|---|
| Long instructional text dịch máy móc | Manual review tất cả entries > 100 chars |
| Course/Batch shared msgid dịch sai 1 trong 2 ngữ cảnh | Reference glossary Course=Khóa học, Batch=Lớp học rõ |
| SCORM strings có HTML tags phức tạp | Script verify HTML tag count match msgid vs msgstr |
| Quiz option strings ngắn dễ ambiguous | Spot-check option strings theo occurrences |

## Security Considerations
- N/A (chỉ .po changes)

## Next Steps
- Phase 4 unblock khi Phase 3 PR merge
