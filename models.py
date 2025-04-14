from typing import List
from pydantic import BaseModel, Field


class FrameDescription(BaseModel):
    """Model for a single frame description."""
    description: str = Field(..., description="Description of what happens in this frame")
    frame_number: int = Field(..., description="Sequential frame number")
    
    
class StoryboardSequence(BaseModel):
    """Model for a sequence of frame descriptions that tell a story."""
    prompt: str = Field(..., description="Original text prompt")
    frames: List[FrameDescription] = Field(default_factory=list, description="List of frame descriptions")
    refined_frames: List[FrameDescription] = Field(default_factory=list, description="List of refined frame descriptions") 