from typing import List, Dict, Any
import cv2
import numpy as np
from pathlib import Path
from ultralytics import YOLO
from app.core.config import get_settings

settings = get_settings()


class DetectionService:
    """Service for object detection using YOLO26 model."""
    
    def __init__(self):
        self.model = None
        # Handle both absolute and relative paths
        model_path = Path(settings.MODEL_PATH)
        if not model_path.is_absolute():
            # If relative, make it relative to project root
            project_root = Path(__file__).parent.parent.parent
            model_path = project_root / model_path
        self.model_path = model_path
        self._load_model()
    
    def _load_model(self):
        """Load YOLO model."""
        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Model file not found at {self.model_path}. "
                "Please ensure the model file exists."
            )
        self.model = YOLO(str(self.model_path))
    
    def detect_objects(
        self,
        image: np.ndarray,
        conf_threshold: float = None,
        iou_threshold: float = None
    ) -> Dict[str, Any]:
        """
        Detect objects in image.
        
        Args:
            image: Input image as numpy array
            conf_threshold: Confidence threshold (default from settings)
            iou_threshold: IoU threshold for NMS (default from settings)
        
        Returns:
            Dictionary containing detection results
        """
        if self.model is None:
            self._load_model()
        
        conf_threshold = conf_threshold or settings.CONFIDENCE_THRESHOLD
        iou_threshold = iou_threshold or settings.IOU_THRESHOLD
        
        # Run inference
        results = self.model.predict(
            image,
            conf=conf_threshold,
            iou=iou_threshold,
            verbose=False
        )
        
        # Process results
        result = results[0]
        detections = []
        
        if result.boxes is not None:
            boxes = result.boxes.xyxy.cpu().numpy()
            confidences = result.boxes.conf.cpu().numpy()
            class_ids = result.boxes.cls.cpu().numpy().astype(int)
            class_names = result.names
            
            for i in range(len(boxes)):
                detections.append({
                    "class_id": int(class_ids[i]),
                    "class_name": class_names[class_ids[i]],
                    "confidence": float(confidences[i]),
                    "bbox": {
                        "x1": float(boxes[i][0]),
                        "y1": float(boxes[i][1]),
                        "x2": float(boxes[i][2]),
                        "y2": float(boxes[i][3])
                    }
                })
        
        # Get annotated image
        annotated_image = result.plot()
        
        return {
            "detections": detections,
            "count": len(detections),
            "annotated_image": annotated_image
        }
    
    def detect_from_bytes(
        self,
        image_bytes: bytes,
        conf_threshold: float = None,
        iou_threshold: float = None
    ) -> Dict[str, Any]:
        """
        Detect objects from image bytes.
        
        Args:
            image_bytes: Image as bytes
            conf_threshold: Confidence threshold
            iou_threshold: IoU threshold
        
        Returns:
            Dictionary containing detection results
        """
        # Decode image
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            raise ValueError("Could not decode image from bytes")
        
        return self.detect_objects(image, conf_threshold, iou_threshold)


# Global service instance
detection_service = DetectionService()

