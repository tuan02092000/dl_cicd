from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import Response, StreamingResponse
import io
import cv2
import numpy as np
from typing import Optional

from app.schemas.detection import DetectionResponse, DetectionRequest
from app.services.detection_service import detection_service

router = APIRouter()


@router.post("/detect", response_model=DetectionResponse)
async def detect_objects(
    file: UploadFile = File(..., description="Image file to process"),
    confidence_threshold: Optional[float] = None,
    iou_threshold: Optional[float] = None
):
    """
    Detect objects in uploaded image.
    
    - **file**: Image file (JPEG, PNG, etc.)
    - **confidence_threshold**: Optional confidence threshold (0.0-1.0)
    - **iou_threshold**: Optional IoU threshold for NMS (0.0-1.0)
    """
    # Validate file type
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    try:
        # Read image bytes
        image_bytes = await file.read()
        
        # Run detection
        result = detection_service.detect_from_bytes(
            image_bytes,
            conf_threshold=confidence_threshold,
            iou_threshold=iou_threshold
        )
        
        # Convert detections to response format
        detections = [
            {
                "class_id": det["class_id"],
                "class_name": det["class_name"],
                "confidence": det["confidence"],
                "bbox": det["bbox"]
            }
            for det in result["detections"]
        ]
        
        return DetectionResponse(
            detections=detections,
            count=result["count"]
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing image: {str(e)}"
        )


@router.post("/detect/image")
async def detect_objects_with_image(
    file: UploadFile = File(..., description="Image file to process"),
    confidence_threshold: Optional[float] = None,
    iou_threshold: Optional[float] = None
):
    """
    Detect objects and return annotated image.
    
    - **file**: Image file (JPEG, PNG, etc.)
    - **confidence_threshold**: Optional confidence threshold (0.0-1.0)
    - **iou_threshold**: Optional IoU threshold for NMS (0.0-1.0)
    
    Returns annotated image with bounding boxes drawn.
    """
    # Validate file type
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    try:
        # Read image bytes
        image_bytes = await file.read()
        
        # Run detection
        result = detection_service.detect_from_bytes(
            image_bytes,
            conf_threshold=confidence_threshold,
            iou_threshold=iou_threshold
        )
        
        # Encode annotated image
        annotated_image = result["annotated_image"]
        _, encoded_image = cv2.imencode(".jpg", annotated_image)
        
        return Response(
            content=encoded_image.tobytes(),
            media_type="image/jpeg"
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing image: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "model_loaded": detection_service.model is not None,
        "model_path": str(detection_service.model_path)
    }

