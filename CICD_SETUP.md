# Hướng dẫn Setup CI/CD cho YOLO26 Object Detection API

Hướng dẫn chi tiết để thiết lập CI/CD pipeline cho dự án lên GitHub.

## 📋 Mục lục

1. [Chuẩn bị](#chuẩn-bị)
2. [Tạo GitHub Repository](#tạo-github-repository)
3. [Push code lên GitHub](#push-code-lên-github)
4. [Cấu hình GitHub Actions](#cấu-hình-github-actions)
5. [Cấu hình Secrets (nếu cần)](#cấu-hình-secrets-nếu-cần)
6. [Kiểm tra CI/CD Pipeline](#kiểm-tra-cicd-pipeline)
7. [Deploy tự động](#deploy-tự-động)

## 🚀 Chuẩn bị

### 1. Cài đặt Git

Đảm bảo Git đã được cài đặt:

```bash
git --version
```

Nếu chưa có, tải tại: https://git-scm.com/downloads

### 2. Cài đặt GitHub CLI (tùy chọn)

```bash
# Windows (choco)
choco install gh

# Hoặc tải từ: https://cli.github.com/
```

## 📦 Tạo GitHub Repository

### Cách 1: Tạo qua GitHub Web

1. Đăng nhập vào [GitHub](https://github.com)
2. Click nút **"+"** ở góc trên bên phải → **"New repository"**
3. Điền thông tin:
   - **Repository name**: `yolo26-object-detection` (hoặc tên bạn muốn)
   - **Description**: "Object Detection API using YOLO26"
   - **Visibility**: Public hoặc Private
   - **Không** tích "Initialize with README" (vì đã có code)
4. Click **"Create repository"**

### Cách 2: Tạo qua GitHub CLI

```bash
gh repo create yolo26-object-detection --public --description "Object Detection API using YOLO26"
```

## 📤 Push code lên GitHub

### Bước 1: Khởi tạo Git repository (nếu chưa có)

```bash
cd D:\Project_TOM\CICD\dl_cicd
git init
```

### Bước 2: Thêm remote repository

```bash
# Thay YOUR_USERNAME và REPO_NAME bằng thông tin của bạn
git remote add origin https://github.com/YOUR_USERNAME/yolo26-object-detection.git

# Hoặc dùng SSH
git remote add origin git@github.com:YOUR_USERNAME/yolo26-object-detection.git
```

### Bước 3: Kiểm tra file .gitignore

Đảm bảo file `.gitignore` đã được tạo và bao gồm:
- `__pycache__/`
- `venv/`
- `.env`
- `*.pyc`
- Model files lớn (nếu cần)

**Lưu ý về Model file:**
- Nếu file `weights/yolo26s.pt` quá lớn (>100MB), GitHub sẽ từ chối
- Có 2 cách xử lý:
  1. **Dùng Git LFS** (Large File Storage):
     ```bash
     git lfs install
     git lfs track "weights/*.pt"
     git add .gitattributes
     ```
  2. **Không commit model file** (uncomment trong .gitignore):
     ```gitignore
     weights/*.pt
     ```
     Và tải model file riêng khi deploy

### Bước 4: Commit và push code

```bash
# Thêm tất cả files
git add .

# Commit
git commit -m "Initial commit: YOLO26 Object Detection API with CI/CD"

# Push lên GitHub
git branch -M main
git push -u origin main
```

## ⚙️ Cấu hình GitHub Actions

### Workflow đã được tạo tự động

File `.github/workflows/ci-cd.yaml` đã được tạo với các jobs:

1. **lint-and-test**: Kiểm tra code quality và chạy tests
2. **build**: Build và verify application
3. **docker-build**: Build Docker image (nếu có Dockerfile)
4. **deploy**: Deploy application (cần cấu hình thêm)

### Workflow sẽ chạy khi:

- Push code lên branch `main`, `master`, hoặc `develop`
- Tạo Pull Request vào `main` hoặc `master`
- Manual trigger qua GitHub Actions tab

## 🔐 Cấu hình Secrets (nếu cần)

Nếu bạn cần deploy tự động hoặc push Docker image, cần cấu hình Secrets:

### Cách thêm Secrets:

1. Vào repository trên GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"**
4. Thêm các secrets cần thiết:

#### Ví dụ: Deploy lên Docker Hub

```
Name: DOCKER_USERNAME
Value: your_dockerhub_username

Name: DOCKER_PASSWORD
Value: your_dockerhub_password
```

#### Ví dụ: Deploy lên Cloud Platform

**AWS:**
```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION
```

**Heroku:**
```
HEROKU_API_KEY
HEROKU_APP_NAME
```

**VPS/Server:**
```
DEPLOY_HOST
DEPLOY_USER
DEPLOY_SSH_KEY
```

## ✅ Kiểm tra CI/CD Pipeline

### 1. Xem workflow runs

1. Vào repository trên GitHub
2. Click tab **"Actions"**
3. Bạn sẽ thấy workflow đang chạy hoặc đã chạy
4. Click vào từng run để xem chi tiết

### 2. Kiểm tra logs

- Click vào job để xem logs chi tiết
- Nếu có lỗi, logs sẽ hiển thị nguyên nhân

### 3. Fix lỗi thường gặp

**Lỗi: Model file không tìm thấy**
- Đây là bình thường trong CI (model không được commit)
- Workflow đã có `continue-on-error: true` để bỏ qua

**Lỗi: Import không tìm thấy**
- Kiểm tra `requirements.txt` đã đầy đủ
- Kiểm tra Python version trong workflow

**Lỗi: Docker build fail**
- Kiểm tra Dockerfile có đúng không
- Kiểm tra context path

## 🚀 Deploy tự động

### Option 1: Deploy với Docker

Workflow đã có job `docker-build`. Để push image:

1. Uncomment phần login Docker Hub trong workflow
2. Thêm Docker Hub secrets
3. Uncomment `push: true` trong build step

### Option 2: Deploy lên Cloud Platform

#### Deploy lên Heroku

Thêm vào workflow:

```yaml
- name: Deploy to Heroku
  uses: akhileshns/heroku-deploy@v3.12.12
  with:
    heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
    heroku_app_name: ${{ secrets.HEROKU_APP_NAME }}
    heroku_email: ${{ secrets.HEROKU_EMAIL }}
```

#### Deploy lên AWS/GCP/Azure

Thêm các bước deploy tương ứng với platform bạn chọn.

### Option 3: Deploy lên VPS/Server

Thêm SSH deploy step:

```yaml
- name: Deploy to Server
  uses: appleboy/ssh-action@master
  with:
    host: ${{ secrets.DEPLOY_HOST }}
    username: ${{ secrets.DEPLOY_USER }}
    key: ${{ secrets.DEPLOY_SSH_KEY }}
    script: |
      cd /path/to/app
      git pull
      docker-compose up -d --build
```

## 📊 Badge Status

Thêm badge vào README.md để hiển thị trạng thái CI/CD:

```markdown
![CI/CD](https://github.com/YOUR_USERNAME/yolo26-object-detection/workflows/CI/CD%20Pipeline/badge.svg)
```

## 🔄 Workflow Triggers

Workflow sẽ chạy tự động khi:

- ✅ Push code
- ✅ Pull Request
- ✅ Manual trigger (workflow_dispatch)

Để chỉnh sửa triggers, sửa phần `on:` trong file workflow.

## 📝 Best Practices

1. **Branch Protection**: Bật branch protection cho `main` branch
2. **Required Checks**: Yêu cầu CI pass trước khi merge
3. **Code Review**: Yêu cầu review trước khi merge
4. **Secrets Management**: Không commit secrets vào code
5. **Docker Caching**: Sử dụng cache để tăng tốc build

## 🆘 Troubleshooting

### Workflow không chạy

- Kiểm tra file có đúng path: `.github/workflows/ci-cd.yaml`
- Kiểm tra syntax YAML
- Kiểm tra branch name trong `on:` trigger

### Tests fail

- Chạy tests local trước: `pytest tests/`
- Kiểm tra dependencies trong `requirements.txt`

### Docker build fail

- Test Dockerfile local: `docker build -t test .`
- Kiểm tra Docker context

## 📚 Tài liệu tham khảo

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

---

**Chúc bạn setup thành công! 🎉**

Nếu có vấn đề, hãy kiểm tra logs trong GitHub Actions tab.

