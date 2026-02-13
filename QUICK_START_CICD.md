# 🚀 Quick Start CI/CD - Hướng dẫn nhanh

## Các bước thực hiện

### 1️⃣ Tạo GitHub Repository

```bash
# Trên GitHub.com: Tạo repository mới (không khởi tạo README)
# Hoặc dùng CLI:
gh repo create yolo26-object-detection --public
```

### 2️⃣ Khởi tạo Git và Push code

```bash
# Trong thư mục dự án
cd D:\Project_TOM\CICD\dl_cicd

# Khởi tạo Git (nếu chưa có)
git init

# Thêm remote (thay YOUR_USERNAME và REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Thêm tất cả files
git add .

# Commit
git commit -m "Initial commit: YOLO26 Object Detection API with CI/CD"

# Push
git branch -M main
git push -u origin main
```

### 3️⃣ Kiểm tra CI/CD

1. Vào repository trên GitHub
2. Click tab **"Actions"**
3. Workflow sẽ tự động chạy
4. Xem kết quả trong vài phút

### 4️⃣ Xử lý Model file lớn (nếu cần)

Nếu file `weights/yolo26s.pt` > 100MB:

**Option A: Dùng Git LFS**
```bash
git lfs install
git lfs track "weights/*.pt"
git add .gitattributes
git commit -m "Add Git LFS for model files"
git push
```

**Option B: Không commit model**
- Uncomment trong `.gitignore`: `weights/*.pt`
- Tải model riêng khi deploy

## ✅ Hoàn thành!

Workflow sẽ tự động chạy mỗi khi bạn:
- Push code mới
- Tạo Pull Request
- Manual trigger

## 📚 Xem thêm

Chi tiết đầy đủ: [CICD_SETUP.md](CICD_SETUP.md)

