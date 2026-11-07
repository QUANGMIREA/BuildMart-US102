# BuildMart US-102: HƯỚNG DẪN THỰC HÀNH TỪ A ĐẾN Z

## 0. Tình trạng bộ mã nguồn

Đã tạo lịch sử Git cục bộ: `main` và `develop` chứa bản baseline V001; `feature/US-102-product-unit` chứa thay đổi V002, API, tests, tài liệu. Chưa tạo task/PR/pipeline trên Azure DevOps và chưa có Azure Run ID. Mọi chỗ cần điền thông tin Azure là phần bạn tự thực hiện.

## 1. Phương pháp thống nhất (dùng xuyên suốt 13 mục)

- Quy trình tạo tài liệu: soạn Markdown theo phần, review chéo, merge, xuất Word.
- Vòng đời phần mềm: **iterative–incremental** (lặp–tăng dần).
- Quản lý công việc: **Kanban** (WIP 2 mỗi lập trình viên, review luồng việc mỗi 2 tuần).
- Thực hành kỹ thuật: **XP** (small changes, unit tests, code review, continuous integration).
- Quản lý nhánh: **Gitflow giản lược** (`main`, `develop`, `feature/US-*`, `release/x.y.z`, `hotfix/x.y.z`).
- Artifact duy nhất: `docs/artifacts/ARTIFACT_REGISTER_RU.md` (A01-A15).
- Release: SemVer; việc merge và việc deployment có approval riêng.
- Phạm vi: V1.0.0 là **bản demo**, chưa thể gọi là cửa hàng thật đã khai trương.

## 2. Chuẩn bị Azure DevOps project

1. Truy cập https://dev.azure.com và đăng nhập, tạo project `BuildMart-SE`, chọn **Agile** process và Git.
2. Tạo repository **trống** tên `BuildMart-US102` (không thêm README mặc định nếu có tùy chọn).
3. Mời 2–4 thành viên khác để đáp ứng yêu cầu nhóm 3–5 người.
4. Trong `Boards > Work Items` hoặc `Boards > Backlogs` tạo hierarchy:
   - Epic: `Каталог строительных материалов`
   - Feature: `Отображение товаров`
   - User Story: `US-102 — Отображение единицы измерения товара`
   - Copy description + AC trong `docs/requirements/US-102_RU.md`.
   - Tạo 5 Task trong bảng của file Story và gán người làm.
5. Giữ mã `US-102` làm mã trình diễn; **ID Work Item Azure do hệ thống cấp khác mã này**, hãy ghi ID thật vào bảng traceability.

## 3. Chạy mã locally

Giải nén project, **mở thư mục có `.git`**. Bắt đầu trên nhánh feature:

```bash
git branch -a
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell:
# .venv\\Scripts\\Activate.ps1
python -m pip install -r requirements.txt
python -m scripts.migrate
python -m pytest -q --junitxml=test-results.xml --cov=app --cov-report=term-missing --cov-report=xml --cov-fail-under=80
python -m uvicorn app.main:app --reload
```

Thử: http://localhost:8000/products, http://localhost:8000/products?unit=мешок, http://localhost:8000/docs. `data/buildmart.db` là demo và bị `.gitignore` bỏ qua.

`test_migrations.py` chứng minh dữ liệu V001 được chuyển thành V002 và migrate lại không tạo thay đổi.

## 4. Đẩy 3 nhánh gốc/feature lên Azure Repos

Lấy **Clone URL** từ trang Azure Repos của repository trống, sau đó chạy:

```bash
git remote add origin <AZURE_REPOS_CLONE_URL>
git push -u origin main
git push -u origin develop
git push -u origin feature/US-102-product-unit
```

Nếu repository Azure đã có commit đầu tiên (README), không force push. Tạo repo mới trống hoặc đồng bộ lịch sử đúng cách.

## 5. Tạo pipeline

1. `Pipelines > New pipeline`.
2. Chọn `Azure Repos Git`, repository `BuildMart-US102`.
3. Chọn `Existing Azure Pipelines YAML file` và nhánh `feature/US-102-product-unit`, file `/azure-pipelines.yml`.
4. `Run` pipeline. Xem từng bước Install -> pytest + coverage -> PublishTestResults -> docker build -> PublishPipelineArtifact.
5. Cần chụp Azure Run ID, số test thật, artifact `buildmart-image`.
6. Nếu Azure báo thiếu hosted parallelism, dùng self-hosted agent có Python và Docker (hoặc yêu cầu cấp hosted capacity). Khả năng chạy trong Azure phụ thuộc tài khoản và agent.

## 6. Branch Policies và Pull Request

1. `Repos > Branches > develop > ... > Branch policies`.
2. Yêu cầu **minimum reviewers = 1**, không cho tự approve nếu có tùy chọn; `Check for linked work items = Required`; `Build validation = Required`, chọn pipeline vừa tạo, Trigger Automatic.
3. Lặp lại chính sách tương ứng cho `main`.
4. `Repos > Pull Requests > New Pull Request`:
   - Source: `feature/US-102-product-unit`
   - Target: `develop`
   - Title: `US-102: Add units for construction materials`
   - Liên kết Work Item Azure thật trong mục Work Items.
   - Reviewer: thành viên QA/PM khác tác giả.
5. Pipeline build validation phải Pass, reviewer duyệt, test thủ công TC-102 được ghi nhận thì mới hoàn thành PR.
6. Sau khi PR merge, đánh dấu User Story Done nếu DoD thỏa đủ.

## 7. Release và deployment demo

1. Trên develop mới nhất tạo `release/1.0.0`. Push branch.
2. CI chạy, QA manual test TC-102 tại staging; điền Test Report.
3. Trước phát hành điền `docs/releases/RELEASE_CHECKLIST_RU.md`.
4. PR `release/1.0.0 -> main`, review + Build Validation.
5. Đồng bộ thay đổi release về develop (PR nếu có thay đổi).
6. Tag trên main: `git tag -a v1.0.0 -m "BuildMart demo v1.0.0"` rồi `git push origin v1.0.0`.
7. Tải artifact `buildmart-image` từ pipeline release/main và mở rộng file `buildmart.tar`.
8. `docker load -i buildmart.tar`, rồi `docker images` để xác định tag `buildmart:<BuildID>`.
9. Chạy: `docker run --rm -d --name buildmart-demo -p 8000:8000 buildmart:<BuildID>`.
10. Kiểm tra /health và /products; điền Deployment Record. Đây là staging/demo không phải production thật.

**Lưu ý Dockerfile cố ý đóng gói SQLite đã migration để demo tự chạy; production thật phải lưu DB bền vững, chạy migration theo approval và không đưa dữ liệu thật vào Docker image.**

## 8. Ảnh minh chứng cần chụp

1. Project settings + team; 2. Epic/Feature/Story hierarchy; 3. US-102 và Task;
4. Git branch list; 5. V001/V002; 6. PR linked to Work Item + reviewer;
7. Branch policy Build Validation; 8. Pipeline run (green); 9. Test results;
10. Pipeline artifact; 11. Manual TC-102 Pass; 12. Release branch/tag;
13. Docker container + /health; 14. Release Checklist + Deployment Record.

## 9. Khả năng kiểm tra chéo giữa lý thuyết và thực hành

Tất cả quy trình ở mục 3 dùng A01-A15; các nhánh mục 5 = nhánh mã thật;
migration mục 6 nằm trong feature và release tương ứng;
unit/auto/manual tests mục 7 có file + results;
release mục 8 có checklist + artifact;
mục 9 chọn B mới mở store, pilot và BCP, **không tuyên bố demo là website thương mại điện tử hoàn chỉnh**.
