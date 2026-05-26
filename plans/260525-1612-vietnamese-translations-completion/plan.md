---
name: vietnamese-translations-completion
date: 2026-05-25
status: in-progress
mode: fast
blockedBy: []
blocks: []
brainstorm: ../reports/brainstorm-260525-1612-vietnamese-translations-completion.md
brainstormExtended: ../reports/brainstormer-260526-1016-vietnamese-i18n-coverage.md
follows: ../260525-1403-language-toggle-en-vi/plan.md
---

# Plan — Vietnamese Translations Completion + Default EN + Hardcoded Audit

## Goal
Hoàn tất Vietnamese i18n end-to-end:
1. Dịch 1360+ chuỗi `msgstr ""` trong `vi.po` (Phase 1-5)
2. Đổi default language toàn hệ thống sang English (Phase 1)
3. Audit + wrap hardcoded English strings trong frontend Vue files (Phase 6 — extended scope từ brainstorm 2026-05-26)
4. Audit + wrap backend Python `frappe._()` calls (Phase 7 — extended scope)
5. Final QA click-through + coverage report (Phase 8 — extended scope)

## Context
- Brainstorm: [report](../reports/brainstorm-260525-1612-vietnamese-translations-completion.md)
- Tiếp nối plan completed: [language-toggle-en-vi](../260525-1403-language-toggle-en-vi/plan.md) — đã build EN/VI toggle, default = VI
- Plan này resolve các Out of Scope của plan cũ: dịch vi.po, đổi default = EN
- Stack: Frappe LMS (Python + Vue 3 + frappe-ui), gettext .po system
- vi.po hiện trạng: 1667 entries, 307 dịch, 1360 trống; main.pot 1707 (thiếu 40 entries trong vi.po)

## Phases

| # | Phase | File | Status |
|---|---|---|---|
| 1 | Foundation: default EN + glossary + .po sync | [phase-01-foundation-default-en.md](phase-01-foundation-default-en.md) | completed |
| 2 | Navigation shell + Modals translations | [phase-02-navigation-shell-translations.md](phase-02-navigation-shell-translations.md) | completed |
| 3 | Learning content translations | [phase-03-learning-content-translations.md](phase-03-learning-content-translations.md) | pending |
| 4 | Batches & community translations | [phase-04-batches-community-translations.md](phase-04-batches-community-translations.md) | pending |
| 5 | Settings + DocType labels + emails translations | [phase-05-settings-doctype-emails-translations.md](phase-05-settings-doctype-emails-translations.md) | pending |
| 6 | Frontend hardcoded strings audit + wrap | [phase-06-frontend-hardcoded-audit.md](phase-06-frontend-hardcoded-audit.md) | pending |
| 7 | Backend Python `frappe._()` audit + wrap | [phase-07-backend-python-audit.md](phase-07-backend-python-audit.md) | pending |
| 8 | Final QA click-through + coverage report | [phase-08-final-qa-coverage.md](phase-08-final-qa-coverage.md) | pending |

## Key Dependencies
- Phase 1 phải merge trước — glossary.md lock terminology, .po sync với .pot
- Phase 2-5 sequential (tránh conflict trên vi.po, mỗi PR commit `chore: Vietnamese translations - <scope>`)
- Phase 6 chạy sau Phase 5 — vi.po phải stable trước khi audit wrap thêm msgid mới
- Phase 7 chạy sau Phase 6 — backend audit reuse glossary + workflow đã established
- Phase 8 chạy cuối — verify toàn bộ stack
- Mỗi PR ship riêng vào `develop`, không gộp vào feature branch tổng

## Files Affected
**Create:**
- `lms/patches/v2_0/set_system_language_en.py`
- `plans/260525-1612-vietnamese-translations-completion/glossary.md` (PR 1)
- `scripts/check-vi-coverage.py` (PR 6 — i18n coverage verification script)

**Modify:**
- `frontend/src/components/LanguageToggle.vue` (default 'vi' → 'en')
- `lms/hooks.py` (User.before_insert thành list, thêm set_default_language)
- `lms/lms/user.py` (thêm hàm `set_default_language`)
- `lms/patches.txt` (register new patch)
- `lms/locale/vi.po` (sync + dịch ~1400 entries qua PR 1-5, + dịch deltas từ Phase 6-7)
- `lms/locale/main.pot` (regen sync ở PR 1, 6, 7)
- 23 Vue files chưa dùng `__()` (Phase 6) + delta files có hardcoded EN (Phase 6)
- Python files trong `lms/**/*.py` có UI-facing strings chưa wrap `frappe._()` (Phase 7)

**Revert sau bench update-translations (PR 1, 6, 7):**
- `lms/locale/{ar,bs,cs,da,de,eo,es,fa,fr,hi,hr,hu,id,it,my,nb,nl,pl,pt,pt_BR,ru,sl,sr,sr_CS,sv,ta,th,tr,zh}.po` (29 files)

## Success Criteria
- Guest / new user → UI hiển thị EN mặc định
- System Settings.language = `en`
- New User created → `User.language = 'en'` (existing users giữ nguyên)
- Toggle VI → tất cả trang trong scope hiển thị tiếng Việt, 0 fallback EN (trừ proper nouns + intentionally-EN technical terms như Quiz/Badge/Webinar)
- `msgfmt --check lms/locale/vi.po` exit 0 sau từng PR
- 307 entries dịch sẵn không bị đổi
- Diff per phase PR < 500 string changes
- **Phase 6:** 100% Vue files có UI text dùng `__()` (verified by `scripts/check-vi-coverage.py`)
- **Phase 7:** 100% Python user-facing strings wrap `frappe._()` (error messages, validation, notifications)
- **Phase 8:** Manual QA pass cho 10 priority pages (Auth, Sidebar, Courses, Lesson, Profile, Notifications, Quiz, Assignment, Batches, Admin) × VI mode

## Out of Scope
- 29 locale khác (ar, de, fr, ...) — stale, không maintain
- Backwards-migrate existing `language='vi'` users về `en` — giữ nguyên user choice
- Frappe framework core strings (không thuộc `lms` app) — out of fork scope
- Crowdin auto-sync — cần manual decide policy (xem Open Questions phía dưới)

## Decisions (locked 2026-05-26)
1. **Crowdin sync policy:** Local override — commit vi.po nội bộ, KHÔNG sync upstream Crowdin. Không pull từ Crowdin trong fork. `bench update-translations lms` chỉ chạy local để extract msgid mới, output diff commit thủ công.
2. **Test environment:** Local `bench start` cho Phase 8 manual QA. Không cần staging URL.
3. **CI integration:** KHÔNG thêm GitHub Action check coverage. Manual review trong PR là đủ cho team size hiện tại.
