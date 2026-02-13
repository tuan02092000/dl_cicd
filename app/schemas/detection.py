from pydantic import BaseModel, Field
from typing import List, Optional


class BBox(BaseModel):
    """Bounding box coordinates."""
    x1: float = Field(..., description="Top-left x coordinate")
    y1: float = Field(..., description="Top-left y coordinate")
    x2: float = Field(..., description="Bottom-right x coordinate")
    y2: float = Field(..., description="Bottom-right y coordinate")


class Detection(BaseModel):
    """Single detection result."""
    class_id: int = Field(..., description="Class ID")
    class_name: str = Field(..., description="Class name")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    bbox: BBox = Field(..., description="Bounding box coordinates")


class DetectionResponse(BaseModel):
    """Response model for detection results."""
    detections: List[Detection] = Field(..., description="List of detections")
    count: int = Field(..., description="Total number of detections")
    message: str = Field(default="Detection completed successfully")


class DetectionRequest(BaseModel):
    """Request model for detection parameters."""
    confidence_threshold: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Confidence threshold for detections"
    )
    iou_threshold: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="IoU threshold for NMS"
    )

