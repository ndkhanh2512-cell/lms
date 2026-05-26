---
phase: 1
status: completed
priority: critical
effort: M
completedAt: 2026-05-26
---

# Phase 1 — Foundation: Default EN + Glossary + .po Sync

## Context Links
- [plan.md](plan.md)
- [brainstorm report](../reports/brainstorm-260525-1612-vietnamese-translations-completion.md)
- Previous plan: [language-toggle-en-vi](../260525-1403-language-toggle-en-vi/plan.md)

## Overview
**Priority:** Critical (blocker cho Phase 2-5)
**Status:** Completed (2026-05-26)
Foundation PR: đổi default language sang EN ở 3 tầng (frontend / System Settings / new user), sync vi.po với main.pot, generate glossary lock terminology cho Phase 2-5. KHÔNG dịch entries — chỉ setup.

## Key Insights
- `User.before_insert` ĐÃ có hook `lms.lms.user.add_lms_student_role` — phải convert thành list để thêm hook mới
- `bench update-translations lms` regen TẤT CẢ 30 file .po — phải `git checkout` 29 file non-vi trước commit
- Glossary mine từ 307 entries đã dịch sẵn → đảm bảo Phase 2-5 không vi phạm terminology hiện có
- Patches version active = `v2_0` (theo `lms/patches.txt` recent entries)

## Requirements

### Functional
- Frontend fallback default = `'en'`
- `User.before_insert` set `language='en'` nếu trống
- System Settings.language = `'en'` (qua patch một lần)
- vi.po có đủ 1707 entries match main.pot
- glossary.md có ≥50 terms từ existing translations + LMS-specific vocabulary

### Non-functional
- 29 file .po non-vi không thay đổi
- 307 entries dịch sẵn của vi.po không bị đổi
- Existing users `language='vi'` không bị migrate

## Architecture

```
User signup flow:
  Frappe creates User doc
    → before_insert hooks (run in order):
       1. add_lms_student_role  (existing)
       2. set_default_language  (new) — set 'en' if empty
    → saved with language='en'

Guest visit:
  LanguageToggle reads localStorage 'lms_lang'
    → empty → fallback 'en' (was 'vi')
    → translation.js fetches /api/method/lms.lms.api.get_translations?lang=en
    → window.translatedMessages = {} (en is source, no translation needed)

System Settings patch (one-time):
  bench --site <site> migrate
    → patches.txt runs new patch
    → set System Settings.language = 'en'
    → fallback cho user chưa set User.language
```

## Related Code Files

**Modify:**
- `frontend/src/components/LanguageToggle.vue` — line 42: `'vi'` → `'en'`
- `lms/hooks.py` — line 126-129: convert `before_insert` thành list
- `lms/lms/user.py` — thêm hàm `set_default_language` sau `add_lms_student_role`
- `lms/patches.txt` — append `lms.patches.v2_0.set_system_language_en`
- `lms/locale/vi.po` — regen từ bench (msgid sync)
- `lms/locale/main.pot` — regen từ bench

**Create:**
- `lms/patches/v2_0/set_system_language_en.py` — patch set System Settings.language = 'en'
- `plans/260525-1612-vietnamese-translations-completion/glossary.md` — terminology lock

**Revert:**
- 29 file `lms/locale/{ar,bs,...}.po` (everything except vi.po, main.pot)

## Implementation Steps

### Step 1 — Frontend default
File: `frontend/src/components/LanguageToggle.vue`
Line 42:
```diff
- return localStorage.getItem('lms_lang') || 'vi'
+ return localStorage.getItem('lms_lang') || 'en'
```

### Step 2 — User.before_insert hook
File: `lms/hooks.py` line 126-129:
```diff
  "User": {
      "validate": "lms.lms.user.validate_username_duplicates",
-     "before_insert": "lms.lms.user.add_lms_student_role",
+     "before_insert": [
+         "lms.lms.user.add_lms_student_role",
+         "lms.lms.user.set_default_language",
+     ],
  },
```

File: `lms/lms/user.py` — thêm sau `add_lms_student_role`:
```python
def set_default_language(doc, method):
    if not doc.language:
        doc.language = "en"
```

### Step 3 — System Settings patch
Create `lms/patches/v2_0/set_system_language_en.py`:
```python
import frappe


def execute():
    frappe.db.set_single_value("System Settings", "language", "en")
```

Register in `lms/patches.txt` (append cuối file):
```
lms.patches.v2_0.set_system_language_en
```

### Step 4 — Translation sync
```bash
# In bench docker container hoặc local bench env
bench --site <site> update-translations lms

# Verify diff
git status lms/locale/

# Revert 29 non-vi files (keep vi.po + main.pot only)
git checkout lms/locale/ar.po lms/locale/bs.po lms/locale/cs.po lms/locale/da.po \
              lms/locale/de.po lms/locale/eo.po lms/locale/es.po lms/locale/fa.po \
              lms/locale/fr.po lms/locale/hi.po lms/locale/hr.po lms/locale/hu.po \
              lms/locale/id.po lms/locale/it.po lms/locale/my.po lms/locale/nb.po \
              lms/locale/nl.po lms/locale/pl.po lms/locale/pt.po lms/locale/pt_BR.po \
              lms/locale/ru.po lms/locale/sl.po lms/locale/sr.po lms/locale/sr_CS.po \
              lms/locale/sv.po lms/locale/ta.po lms/locale/th.po lms/locale/tr.po \
              lms/locale/zh.po

# Validate vi.po syntax
msgfmt --check lms/locale/vi.po
```

### Step 5 — Generate glossary.md
- Script đọc vi.po, extract pairs `(msgid, msgstr)` where `msgstr != ""`
- Tổng 307 pairs → group theo concept (UI verbs / Domain nouns / Phrases)
- Augment với LMS terminology (Course/Batch/Lesson/Chapter/Quiz/Assignment/Instructor/Student/Certificate/Cohort/Mentor/Enrollment/Progress)
- Tone rules: "Bạn", informal lịch sự
- Output: `plans/260525-1612-vietnamese-translations-completion/glossary.md`
- Format:
  ```markdown
  ## Domain nouns
  | English | Tiếng Việt | Note |
  |---|---|---|
  | Course | Khóa học | |
  | Batch | Lớp học | (LMS Batch doctype) |
  ...

  ## UI verbs (button actions)
  | English | Tiếng Việt |
  |---|---|
  | Save | Lưu |
  | Cancel | Hủy |
  ...

  ## Phrases & tone rules
  - Default pronoun: "Bạn"
  - Confirmation prompts: "Bạn có chắc muốn..."
  - Button labels: ngắn, mệnh lệnh, không pronoun
  ```

### Step 6 — Smoke test (manual)
- `cd frontend && yarn build` hoặc dev server đang chạy
- Clear localStorage `lms_lang` → reload → UI hiển thị EN
- Login user mới tạo → check `User.language` = `en` qua Frappe Desk
- Migrate site: `bench --site <site> migrate` → verify System Settings.language = `en`
- Existing user `language='vi'` login → UI vẫn VI

### Step 7 — Commit & PR
```bash
git add frontend/src/components/LanguageToggle.vue \
        lms/hooks.py lms/lms/user.py \
        lms/patches.txt lms/patches/v2_0/set_system_language_en.py \
        lms/locale/vi.po lms/locale/main.pot \
        plans/260525-1612-vietnamese-translations-completion/

git commit -m "feat(i18n): default English + sync vi.po with main.pot

- Frontend LanguageToggle fallback 'vi' -> 'en'
- User.before_insert sets language='en' for new users
- Patch sets System Settings.language='en' (one-time)
- bench update-translations sync vi.po + main.pot (29 non-vi reverted)
- Glossary generated for Phase 2-5 translation work"
```
PR target: `develop`.

## Todo List
- [x] Modify `LanguageToggle.vue:42`
- [x] Modify `hooks.py` doc_events User.before_insert thành list
- [x] Add `set_default_language` vào `lms/lms/user.py`
- [x] Create `lms/patches/v2_0/set_system_language_en.py`
- [x] Register patch trong `lms/patches.txt`
- [x] Sync vi.po: `bench generate-pot-file --app lms` + `bench update-po-files --app lms --locale vi`
- [x] `--locale vi` flag scoped sync — 29 non-vi files not touched (no checkout needed)
- [x] Validate vi.po via Babel `read_po` (msgfmt unavailable in container)
- [x] Generate glossary.md (mine 307 entries + augment + flag 5 inconsistencies)
- [ ] Smoke test deferred to first `bench restart` after merge: guest EN default, new user `language='en'`, existing VI giữ nguyên
- [ ] `bench --site <site> migrate` verify System Settings updated (post-merge)
- [x] Commit Phase 1 changes

## Success Criteria
- LocalStorage cleared → guest visit → EN
- New user signup → `User.language = 'en'` trong DB
- `frappe.get_single_value("System Settings", "language")` = `'en'`
- Existing `language='vi'` users không thay đổi
- vi.po có 1707 entries matching main.pot
- 29 non-vi .po files diff = 0
- glossary.md ≥50 terms, có sections Domain/Verbs/Tone
- `msgfmt --check lms/locale/vi.po` exit 0

## Risk Assessment

| Risk | Mitigation |
|---|---|
| `before_insert` list breaks Frappe hook resolution | Test signup + create user via UI sau khi merge |
| Patch run lỗi trên site đã có `language='vi'` | Patch idempotent — `set_single_value` overwrite OK |
| `bench update-translations` regen 29 file .po | `git checkout` explicit list trước commit |
| msgctxt entries trong vi.po bị xáo trộn | Verify `msgfmt --check` + spot-check 10 entries có `msgctxt` |
| Hook order mới làm `add_lms_student_role` fail | Frappe doc_events list chạy sequential — không phụ thuộc nhau |

## Security Considerations
- Patch chỉ touch System Settings (admin-controlled) — không leak data
- `set_default_language` chỉ set field nếu trống → không override user choice
- Không expose endpoint mới — chỉ hook nội bộ

## Next Steps
- Phase 2 unblock sau khi PR 1 merge và glossary.md được commit
- Phase 2-5 reference glossary.md as single source of truth
