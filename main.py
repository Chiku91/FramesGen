from typing import List, Optional

from .llm_service import LLMService
from .image_service import ImageGenerationService
from .models import StoryboardSequence


def process_prompt(prompt: str, num_frames: int = 5) -> StoryboardSequence:
    """
    Process a text prompt into a sequence of video frame descriptions.
    
    Args:
        prompt: The text prompt to convert into frame descriptions
        num_frames: The number of frames to generate
        
    Returns:
        A StoryboardSequence containing the original prompt, generated frames,
        and refined frames for better coherence
    """
    # Initialize LLM service
    llm_service = LLMService()
    
    # Create storyboard sequence object
    storyboard = StoryboardSequence(prompt=prompt)
    
    # Step 1: Generate initial frame sequence
    frames = llm_service.generate_frame_sequence(prompt, num_frames)
    storyboard.frames = frames
    
    # Step 2: Refine frame sequence for consistency and coherence
    refined_frames = llm_service.refine_frame_sequence(frames, prompt)
    storyboard.refined_frames = refined_frames
    
    return storyboard


def generate_images_for_storyboard(storyboard: StoryboardSequence, 
                                  style_prompt: str = "high quality, detailed, cinematic lighting",
                                  negative_prompt: str = "blurry, low quality, distorted, deformed") -> List[str]:
    """
    Generate images for the refined frame descriptions in a storyboard.
    
    Args:
        storyboard: The StoryboardSequence containing frame descriptions
        style_prompt: Additional style guidance to add to all prompts
        negative_prompt: Things to avoid in all images
        
    Returns:
        List of paths to generated images
    """
    # Initialize image service
    image_service = ImageGenerationService()
    
    # Generate images for refined frames (they're better than the initial frames)
    return image_service.generate_frame_images(
        storyboard.refined_frames, 
        style_prompt=style_prompt,
        negative_prompt=negative_prompt
    ) 