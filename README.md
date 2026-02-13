# YOLO26 Object Detection API

Ứng dụng Object Detection sử dụng mô hình YOLO26 từ Ultralytics với giao diện web demo và REST API.

## Tính năng

- 🎯 Object Detection với YOLO26 model
- 🌐 REST API với FastAPI
- 💻 Web Demo với giao diện đẹp
- ⚡ Xử lý bất đồng bộ (async)
- 📊 Hiển thị kết quả detection với bounding boxes
- 🎨 Giao diện responsive, hỗ trợ drag & drop

## Cài đặt

### 1. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 2. Đảm bảo model file tồn tại

Đảm bảo file model `weights/yolo26s.pt` đã có trong thư mục `weights/`.

### 3. Cấu hình (tùy chọn)

Sao chép file `.env.example` thành `.env` và chỉnh sửa nếu cần:

```bash
cp .env.example .env
```

## Chạy ứng dụng

### Chạy server

```bash
# Sử dụng uvicorn trực tiếp
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Hoặc chạy từ Python
python -m app.main
```

### Truy cập

- **Web Demo**: http://localhost:8000/demo hoặc http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

## API Endpoints

### 1. Detect Objects (JSON Response)

**POST** `/api/v1/detection/detect`

Upload image và nhận kết quả detection dưới dạng JSON.

**Parameters:**
- `file`: Image file (multipart/form-data)
- `confidence_threshold` (optional): Ngưỡng confidence (0.0-1.0)
- `iou_threshold` (optional): Ngưỡng IoU cho NMS (0.0-1.0)

**Response:**
```json
{
  "detections": [
    {
      "class_id": 0,
      "class_name": "person",
      "confidence": 0.95,
      "bbox": {
        "x1": 100.0,
        "y1": 150.0,
        "x2": 300.0,
        "y2": 500.0
      }
    }
  ],
  "count": 1,
  "message": "Detection completed successfully"
}
```

### 2. Detect Objects (Annotated Image)

**POST** `/api/v1/detection/detect/image`

Upload image và nhận ảnh đã được vẽ bounding boxes.

**Parameters:**
- `file`: Image file (multipart/form-data)
- `confidence_threshold` (optional): Ngưỡng confidence (0.0-1.0)
- `iou_threshold` (optional): Ngưỡng IoU cho NMS (0.0-1.0)

**Response:** Image file (JPEG) với bounding boxes đã được vẽ

### 3. Health Check

**GET** `/api/v1/detection/health`

Kiểm tra trạng thái API và model.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_path": "weights/yolo26s.pt"
}
```

## Sử dụng API với cURL

### Detect objects (JSON)

```bash
curl -X POST "http://localhost:8000/api/v1/detection/detect" \
  -F "file=@path/to/image.jpg" \
  -F "confidence_threshold=0.25" \
  -F "iou_threshold=0.45"
```

### Detect objects (Image)

```bash
curl -X POST "http://localhost:8000/api/v1/detection/detect/image" \
  -F "file=@path/to/image.jpg" \
  -o result.jpg
```

## Sử dụng với Python

```python
import requests

# Detect objects
with open("image.jpg", "rb") as f:
    response = requests.post(
        "http://localhost:8000/api/v1/detection/detect",
        files={"file": f},
        data={"confidence_threshold": 0.25}
    )
    
result = response.json()
print(f"Found {result['count']} objects")
for det in result['detections']:
    print(f"{det['class_name']}: {det['confidence']:.2%}")
```

## Cấu trúc dự án

```
.
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   └── detection.py
│   │       └── router.py
│   ├── core/
│   │   └── config.py
│   ├── schemas/
│   │   └── detection.py
│   ├── services/
│   │   └── detection_service.py
│   └── main.py
├── static/
│   └── demo.html
├── weights/
│   └── yolo26s.pt
├── requirements.txt
├── .env.example
└── README.md
```

## Docker

### Build và chạy với Docker

```bash
# Build image
docker build -t yolo26-detection .

# Chạy container
docker run -p 8000:8000 yolo26-detection
```

### Sử dụng Docker Compose

```bash
# Chạy với docker-compose
docker-compose up -d

# Xem logs
docker-compose logs -f

# Dừng
docker-compose down
```

## CI/CD

Dự án đã được cấu hình CI/CD với GitHub Actions. Xem chi tiết tại [CICD_SETUP.md](CICD_SETUP.md).

### Workflow bao gồm:

- ✅ **Lint & Test**: Kiểm tra code quality và chạy tests
- ✅ **Build**: Build và verify application
- ✅ **Docker Build**: Build Docker image
- ✅ **Deploy**: Deploy tự động (cần cấu hình)

### Quick Start CI/CD:

1. Push code lên GitHub repository
2. Workflow sẽ tự động chạy khi push/PR
3. Xem kết quả tại tab **Actions** trên GitHub

## Công nghệ sử dụng

- **FastAPI**: Web framework hiện đại, nhanh
- **Ultralytics YOLO**: Mô hình object detection
- **OpenCV**: Xử lý ảnh
- **Pydantic**: Validation và serialization
- **Uvicorn**: ASGI server
- **Docker**: Containerization
- **GitHub Actions**: CI/CD pipeline

## Testing

```bash
# Cài đặt test dependencies
pip install pytest pytest-asyncio httpx

# Chạy tests
pytest tests/ -v
```

## License

MIT

