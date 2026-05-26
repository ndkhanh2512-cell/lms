---
phase: 5
status: pending
priority: medium
effort: M
blockedBy: [phase-04]
---

# Phase 5 — Settings + DocType Labels + Emails Translations

## Context Links
- [plan.md](plan.md)
- [phase-04-batches-community-translations.md](phase-04-batches-community-translations.md)
- [glossary.md](glossary.md)

## Overview
**Priority:** Medium
**Status:** Pending
Final phase. Dịch ~200-300 chuỗi vi.po còn lại: Profile/Settings pages, DocType JSON labels, email templates, www public pages. Hoàn tất 100% vi.po (trừ entries có flag `#, fuzzy` và proper nouns).

## Key Insights
- DocType labels có comment dạng `#. Label of the X (Y) field in DocType 'Z'` — đọc context để dịch label phù hợp
- Email templates (`lms/templates/emails/*.html`) có entries `_("...")` Jinja → Frappe extract vào .po, dịch trong .po là đủ
- `lms/www/` là Frappe website templates → dịch tương tự
- Một số label DocType cố ý ngắn (e.g. "ID", "Type") → giữ ngắn, không tự ý mở rộng

## Requirements

### Functional
- Tất cả msgid còn lại trong vi.po `msgstr ""` → dịch xong (trừ proper nouns / fuzzy)
- Terminology nhất quán glossary
- Email/template placeholder Jinja `{{ user.first_name }}` preserve

### Non-functional
- `msgfmt --check` exit 0
- Sau Phase 5, `grep 'msgstr ""' lms/locale/vi.po` chỉ còn entries proper noun / fuzzy
- Smoke test settings + 1 email gửi thử

## Scope (File Path Filter)

- `frontend/src/pages/Profile/`
- `frontend/src/components/Profile*`
- `frontend/src/pages/Settings/`
- `frontend/src/components/Settings/`
- `lms/lms/doctype/` (tất cả `.json` labels via `#. Label of...` comments)
- `lms/templates/emails/` (welcome, batch_confirmation, certificate_email, ...)
- `lms/www/` (public web pages, statistics, contact)
- `lms/templates/` (other Jinja templates)
- Bất kỳ entry còn lại không thuộc Phase 2-4 (catch-all)

## Workflow

### Step 1 — Extract remaining empty entries
Sau Phase 4 merge: list tất cả entries `msgstr ""` còn lại = scope Phase 5 (catch-all).
```python
import polib
po = polib.pofile("lms/locale/vi.po")
todo = [e for e in po if not e.msgstr.strip() and 'fuzzy' not in e.flags]
```

### Step 2 — Split theo loại
- DocType labels (có `#. Label of...` comment) → batch riêng, prompt subagent đọc DocType name + field type
- Email templates (path `lms/templates/emails/`) → batch riêng, preserve Jinja `{{ }}` tags
- Settings/Profile UI → batch riêng
- Catch-all còn lại → batch cuối

### Step 3 — Translate batches qua subagent
Special instructions cho subagent:
- DocType labels: ngắn gọn, dùng noun (vd "Email Address" → "Địa chỉ Email")
- Email body: lịch sự, dùng "Bạn", giữ tone formal hơn UI
- Jinja `{{ }}` tags preserve exact

### Step 4 — Apply + validate
Same as Phase 2-4.

### Step 5 — Manual review
- TẤT CẢ DocType labels: review tay (sai 1 label có thể confuse user mãi)
- TẤT CẢ email templates: review tay (gửi production)
- Catch-all > 100 chars

### Step 6 — Smoke test
- Profile page (view, edit)
- Settings page (tất cả tabs: general, notifications, branding, integrations, transactions)
- Tạo trigger 1 email: enroll batch → check `frappe.local.email_queue` hoặc preview email với `bench --site X console`
- Browse 1-2 trang www public (e.g. `/lms/courses`, `/lms/statistics`)
- Frappe Desk view 1 DocType form (e.g. LMS Course) → check field labels VI

### Step 7 — Commit
```bash
git commit -m "chore: Vietnamese translations - settings, doctype labels, emails"
```

## Todo List
- [ ] Extract remaining empty entries
- [ ] Split batches: DocType / Email / Settings UI / Catch-all
- [ ] Translate qua subagent (4 batches)
- [ ] Apply + msgfmt --check
- [ ] Manual review TẤT CẢ DocType labels + email templates
- [ ] Spot-check catch-all
- [ ] Smoke test Profile/Settings UI
- [ ] Smoke test email preview
- [ ] Smoke test DocType form qua Frappe Desk
- [ ] Smoke test www public pages
- [ ] Commit + PR

## Success Criteria
- `grep 'msgstr ""' lms/locale/vi.po | wc -l` = số entries fuzzy / proper noun (gần 0)
- Profile/Settings page hoàn toàn tiếng Việt
- Email "Welcome / Batch Confirmation / Certificate" preview tiếng Việt natural
- DocType labels trên Frappe Desk (LMS Course, LMS Batch, ...) tiếng Việt
- `msgfmt --check` exit 0
- Diff = ~200-300 msgstr changes

## Risk Assessment

| Risk | Mitigation |
|---|---|
| DocType label dịch sai gây confuse admin | Review TẤT CẢ labels tay (~80-100 entries) |
| Email Jinja tags `{{ user.X }}` bị phá | Script verify `{{ }}` count match + render test |
| Catch-all bao gồm web template strings có HTML phức | Spot-check HTML-heavy entries |
| Một số label được Frappe app khác share (Frappe core, ERPNext) | Chỉ dịch trong lms/locale/vi.po, không động app khác |
| Email gửi production sai grammar embarrassing | Review tay 100% email templates trước commit |

## Security Considerations
- Email templates render với user data → preserve Jinja escape không cho XSS
- Không expose endpoint mới

## Next Steps
- Plan completed sau Phase 5 merge
- Run `/ck:plan archive` để journal + archive plan
- Optional follow-up: wrap hardcoded English strings với `__()` (separate plan)
- Optional: maintain 29 locale khác (separate plan, low priority)
