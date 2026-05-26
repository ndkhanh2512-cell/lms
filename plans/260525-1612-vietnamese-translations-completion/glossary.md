# Vietnamese i18n Glossary — LMS

Single source of truth for VI terminology. Phase 2-5 PRs MUST conform.

Sources:
- Mined from 307 existing `(msgid, msgstr)` pairs in `lms/locale/vi.po` (synced 2026-05-26 via `bench update-po-files --app lms --locale vi`).
- Augmented with LMS-specific vocabulary (Course, Batch, Lesson, Chapter, Quiz, Assignment, Certificate, Cohort, Mentor, Enrollment, Progress, Webinar, Badge — some kept English by design).

Tone:
- Pronoun: **"Bạn"** (informal lịch sự). Never use "anh/chị" or "quý vị".
- Button labels: ngắn, mệnh lệnh (no pronoun). "Lưu", "Hủy", "Xóa".
- Confirmations: "Bạn có chắc muốn..." / "Bạn có muốn..."
- Email greetings: "Xin chào" (formal), "Chào" (casual), "Kính gửi" (very formal — emails to instructors/admins).
- Empty states + onboarding: ngắn gọn, hành động + danh từ ("Tạo khóa học đầu tiên").

Locked exceptions — keep English (proper nouns / technical / brand):
- Frappe, Frappe Learning, GitHub, LinkedIn, Twitter, GSTIN, PAN, PDF, UUID, URL, JavaScript, HTML
- Quiz / Webinar / Badge — domain-specific, intentionally English in product copy

---

## Domain nouns

| English | Tiếng Việt | Note |
|---|---|---|
| Course | Khóa học | Plural "Khóa học" (no marker) |
| Courses | Khóa học | |
| Course Name | Tên khóa học | |
| Batch | Lớp học | LMS Batch doctype; never "lô" |
| Batches | Lớp học | |
| Batch Details | Chi tiết lớp học | Override existing "Chi tiết lô" — wrong |
| Lesson | Bài học | |
| Chapter | Chương | |
| Quiz | Bài kiểm tra | "Quizzes" → "Bài kiểm tra" |
| Assignment | Bài tập | Single submission item |
| Assignments | Nhiệm vụ được giao | Tab/section label |
| Assessment | Đánh giá | "Assessments" → "Đánh giá" |
| Certificate | Chứng chỉ | "Certifications" → "Chứng chỉ" |
| Certification | Chứng nhận | When = process / act of certifying |
| Certified | Được chứng nhận | |
| Instructor | Giảng viên | "Instructors" → "Giảng viên" |
| Student | Học viên | **Override** existing "Sinh viên" — LMS uses học viên |
| Students | Học viên | |
| Member | Thành viên | |
| Members | Thành viên | |
| Member Name | Tên thành viên | |
| Mentor | Cố vấn | |
| Enrollment | Đăng ký | |
| Enrolled | Đã đăng ký | |
| Progress | Tiến độ | |
| Programming Exercises | Bài tập lập trình | |
| Event | Sự kiện | |
| Job | Việc làm | "Jobs" → "Việc làm" |
| Program | Chương trình | "Programs" → "Chương trình" |
| Announcements | Thông báo | |
| Notifications | Thông báo | |
| Discussion | Thảo luận | |
| Webinar | Webinar | Keep English |
| Badge | Badge | Keep English |

## Status & state nouns

| English | Tiếng Việt |
|---|---|
| Status | Trạng thái |
| In Progress | Đang tiến hành |
| Completed | Đã hoàn thành |
| Complete | Hoàn thành |
| Cancelled | Đã hủy |
| Closed | Đã đóng |
| Open | Mở |
| Published | Đã xuất bản |
| Approved | Đã được phê duyệt |
| Pending | Đang chờ xử lý |
| Pass | Vượt qua |
| Fail / Failed | Thất bại |
| Archived | Đã lưu trữ |
| Disabled | Đã tắt |
| Enabled | Đã bật |

## UI verbs (button actions)

| English | Tiếng Việt |
|---|---|
| Save | Lưu |
| Cancel | Hủy |
| Delete | Xóa  **(override)** existing wrong msgstr |
| Edit | Chỉnh sửa |
| Update | Cập nhật |
| Create | Tạo |
| Create New | Tạo mới |
| Add | Thêm |
| Remove | Xóa |
| Submit | Gửi |
| Send | Gửi |
| Apply | Áp dụng |
| Confirm | Xác nhận |
| Close | Đóng |
| Clear | Xóa |
| Search | Tìm kiếm |
| Next | Tiếp theo |
| Previous | Trước |
| Skip | Bỏ qua |
| Start | Bắt đầu |
| Resume | Tiếp tục |
| Upload | Tải lên |
| Login | Đăng nhập |
| Sign up | Đăng ký |
| Join | Tham gia |
| Discard | Loại bỏ |
| Try Again | Thử lại |
| Load More | Tải thêm |
| Expand | Mở rộng |
| Collapse | Thu gọn |
| Run | Chạy |
| Post | Đăng |

## Form & field labels

| English | Tiếng Việt |
|---|---|
| Name | Tên |
| Title | Tiêu đề |
| Description | Mô tả |
| Type | Loại |
| Category | Thể loại |
| Tags | Thẻ |
| Date | Ngày |
| Time | Thời gian |
| Duration | Thời gian |
| Start Date | Ngày bắt đầu |
| End Date | Ngày kết thúc |
| From Date | Từ Ngày |
| To Date | Đến Ngày |
| Phone Number | Số điện thoại |
| Email ID | ID email |
| Username | Tên người dùng |
| Password | Mật khẩu |
| Full Name | Tên đầy đủ |
| First Name | Tên |
| Last Name | Họ |
| Bio | Tiểu sử |
| Address | Địa chỉ |
| Country | Quốc gia |
| City | Thành phố |
| Postal Code | Mã Bưu Chính |
| State/Province | Tỉnh/Thành phố |
| Company | Công ty |
| Currency | Tiền tệ |
| Total | Tổng cộng |
| Subject | Chủ đề |
| Message | Tin nhắn |

## Roles & user

| English | Tiếng Việt |
|---|---|
| User | Người dùng |
| Users | Người dùng |
| Owner | Chủ sở hữu |
| Role | Vai trò |
| Roles | Vai trò |
| Administrator | Quản trị viên |
| System Manager | Người quản lý hệ thống |
| Evaluator | Người đánh giá |
| Moderator | Người kiểm duyệt |

## Navigation & layout

| English | Tiếng Việt |
|---|---|
| Home | Trang chủ |
| Dashboard | Trang tổng quan |
| Sidebar | Thanh bên |
| Settings | Thiết lập |
| Help | Trợ giúp |
| Profile | Hồ sơ |
| My Profile | Hồ sơ của tôi |
| Overview | Tổng quan |
| Details | Chi tiết |
| Statistics | Thống kê |
| Feedback | Phản hồi |
| About | Giới thiệu về |
| Contact Us | Liên hệ với chúng tôi |

## Common phrases & system messages

| English | Tiếng Việt |
|---|---|
| Hello | Xin chào |
| Hey | Chào |
| Dear | Kính gửi |
| Regards | Trân trọng |
| Not Allowed | Không được phép |
| Not Permitted | Không được phép |
| Not Applicable | Không áp dụng |
| Not Saved | Chưa được lưu |
| No results found | Không tìm thấy kết quả nào |
| Email sent successfully | Email đã được gửi thành công |
| Already Registered | Đã Đăng Ký |
| Temporarily Disabled | Tạm thời bị vô hiệu hóa |
| Sign Up is disabled | Đăng ký bị vô hiệu hóa |
| Powered by Frappe Learning | Phát triển bởi Frappe Learning |
| Click here | Bấm vào đây |
| You are not permitted to access this page. | Bạn không được phép truy cập trang này. |

## Empty-state / onboarding CTAs

| English | Tiếng Việt |
|---|---|
| Create your first course | Tạo khóa học đầu tiên |
| Create your first batch | Tạo lớp học đầu tiên |
| Create your first quiz | Tạo bài kiểm tra đầu tiên |
| Add your first chapter | Thêm chương đầu tiên |
| Add your first lesson | Thêm bài học đầu tiên |
| Add courses to your batch | Thêm khóa học vào lớp |
| Add students to your batch | Thêm học viên vào lớp |
| Invite your team and students | Mời nhóm và học viên |
| Complete your profile | Hoàn thiện hồ sơ |
| Manage your courses and batches at a glance | Quản lý khóa học và lớp học của bạn ngay tại đây |

## Days of week

| English | Tiếng Việt |
|---|---|
| Monday | Thứ Hai |
| Tuesday | Thứ Ba |
| Wednesday | Thứ Tư |
| Thursday | Thứ Năm |
| Friday | Thứ Sáu |
| Saturday | Thứ Bảy |
| Sunday | Chủ Nhật |

## Colors (used in tag/badge picker)

Amber, Blue, Cyan, Gray, Green, Orange, Pink, Purple, Red, Yellow — see existing 307 entries; keep mapping consistent.

---

## Inconsistencies in pre-existing translations — fix during Phase 2-5

| msgid | Existing msgstr | Recommended fix |
|---|---|---|
| Delete | "Đã cập nhật giá trị mặc định" (wrong, copy-paste error) | "Xóa" |
| Student | "Sinh viên" | "Học viên" (LMS context) |
| Students | "Sinh viên" | "Học viên" |
| Batch Details | "Chi tiết lô" | "Chi tiết lớp học" |
| First Name | "Họ Tên" | "Tên" |

When updating an already-translated msgstr above, note it in the PR description so reviewer can verify.

---

## Stylistic rules

1. **Capitalize** Vietnamese sentences as standard prose. Don't title-case Vietnamese.
2. **Punctuation:** preserve trailing English punctuation (`.`, `!`, `?`, `:`). Spaces around `{0}` placeholders: copy from English exactly.
3. **Placeholders {0}, {1}:** keep position natural to Vietnamese grammar (e.g., `"New {0}"` → `"{0} mới"` if more natural; else keep `"Mới {0}"`).
4. **Plural vs singular:** Vietnamese has no number marker. Translate plural form same as singular UNLESS context demands quantifier (e.g., "3 students" → "3 học viên").
5. **Email body strings:** prefer formal "Kính gửi"/"Trân trọng" framing. Match existing email .html templates' tone.
6. **Doctype labels (msgctxt):** when same msgid has `msgctxt`, treat each as independent entry — translation may differ by context.
7. **HTML strings (in .html templates):** keep HTML tags intact, translate only text nodes.

## Process

- Each Phase 2-5 PR opens a separate scope (Navigation/Modals, Learning, Batches, Settings/DocType/Emails).
- Diff per PR < 500 string changes.
- Before commit: `bench update-po-files --app lms --locale vi` to re-canonicalize order if file was hand-edited (optional — Babel preserves order on `msgmerge`).
- Validate: `python -c "from babel.messages.pofile import read_po; read_po(open('lms/locale/vi.po','rb'))"` must not raise.
- Reviewer checks PR diff for glossary conformance.
