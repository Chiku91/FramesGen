import os
import io
import time
import base64
import requests
from typing import List, Optional
from PIL import Image
from datetime import datetime

from .config import STABILITY_API_KEY
from .models import FrameDescription


class ImageGenerationService:
    """Service for generating images from frame descriptions using Stability AI."""
    
    def __init__(self):
        self.api_key = STABILITY_API_KEY
        self.api_host = 'https://api.stability.ai'
        self.engine_id = 'stable-diffusion-xl-1024-v1-0'  # SDXL 1.0
        
        # Create output directory if it doesn't exist
        self.output_dir = os.path.join(os.getcwd(), "generated_frames")
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_image(self, prompt: str, negative_prompt: str = None) -> Optional[Image.Image]:
        """
        Generate an image from a text prompt using Stability AI.
        
        Args:
            prompt: The text prompt to generate an image from
            negative_prompt: Things to avoid in the image (optional)
            
        Returns:
            A PIL Image object, or None if generation failed
        """
        if not self.api_key:
            print("Error: Stability API key is not set.")
            return None
        
        url = f"{self.api_host}/v1/generation/{self.engine_id}/text-to-image"
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        
        body = {
            "text_prompts": [
                {
                    "text": prompt,
                    "weight": 1.0
                }
            ],
            "cfg_scale": 7.0,
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 30,
        }
        
        # Add negative prompt if provided
        if negative_prompt:
            body["text_prompts"].append({
                "text": negative_prompt,
                "weight": -1.0
            })
        
        try:
            response = requests.post(url, headers=headers, json=body)
            
            if response.status_code != 200:
                print(f"Error: Non-200 response: {response.text}")
                return None
                
            data = response.json()
            
            if "artifacts" in data and len(data["artifacts"]) > 0:
                image_data = base64.b64decode(data["artifacts"][0]["base64"])
                return Image.open(io.BytesIO(image_data))
            
            return None
            
        except Exception as e:
            print(f"Error generating image: {e}")
            return None
            
    def save_image(self, image: Image.Image, filename: str) -> str:
        """
        Save an image to disk.
        
        Args:
            image: The PIL Image to save
            filename: Base filename to use
            
        Returns:
            The path to the saved image
        """
        if not image:
            return None
            
        # Clean up filename and add timestamp
        clean_filename = "".join(c if c.isalnum() or c in [' ', '-', '_'] else '_' for c in filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        full_filename = f"{timestamp}_{clean_filename}.png"
        
        file_path = os.path.join(self.output_dir, full_filename)
        image.save(file_path)
        
        return file_path
    
    def generate_frame_images(self, frames: List[FrameDescription], 
                              style_prompt: str = "high quality, detailed, cinematic lighting", 
                              negative_prompt: str = "blurry, low quality, distorted, deformed") -> List[str]:
        """
        Generate images for a sequence of frame descriptions.
        
        Args:
            frames: List of frame descriptions to generate images for
            style_prompt: Additional style guidance to add to all prompts
            negative_prompt: Things to avoid in all images
            
        Returns:
            List of paths to generated images
        """
        image_paths = []
        
        for i, frame in enumerate(frames):
            print(f"Generating image for frame {frame.frame_number}/{len(frames)}: {frame.description[:50]}...")
            
            # Create a full prompt with style guidance
            full_prompt = f"{frame.description}. {style_prompt}"
            
            # Generate the image
            image = self.generate_image(full_prompt, negative_prompt)
            
            if image:
                # Save the image with a descriptive name
                filename = f"frame_{frame.frame_number:02d}_{frame.description[:30].replace(' ', '_')}"
                image_path = self.save_image(image, filename)
                
                if image_path:
                    print(f"Saved image: {image_path}")
                    image_paths.append(image_path)
            
            # Prevent rate limiting issues
            if i < len(frames) - 1:
                time.sleep(1)
        
        return image_paths 