import requests
from typing import List, Dict, Any

from .config import HF_API_TOKEN, MODEL_NAME
from .models import FrameDescription, StoryboardSequence

class LLMService:
    """Service for interacting with Hugging Face's API."""
    
    def __init__(self):
        self.api_url = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"
        self.headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
        self.model = MODEL_NAME
    
    def call_llm(self, messages: List[Dict[str, Any]]) -> str:
        """Call the LLM with the given messages and return the response."""
        
        # Convert messages to a format that Hugging Face models understand
        # This is a simplified template for text generation models
        prompt = self._format_messages(messages)
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 512,
                "temperature": 0.7,
                "do_sample": True
            }
        }
        
        response = requests.post(self.api_url, headers=self.headers, json=payload)
        
        if response.status_code != 200:
            raise ValueError(f"Error from Hugging Face API: {response.text}")
        
        # Extract the generated text from the response
        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            # Some models return a list of generation results
            return result[0].get("generated_text", "").replace(prompt, "").strip()
        elif isinstance(result, dict):
            # Some models return a dictionary
            return result.get("generated_text", "").replace(prompt, "").strip()
        
        return "Error: Unexpected response format"
    
    def _format_messages(self, messages: List[Dict[str, Any]]) -> str:
        """Format messages into a prompt that Hugging Face models can understand."""
        formatted_prompt = ""
        
        for message in messages:
            role = message.get("role", "")
            content = message.get("content", "")
            
            if role == "system":
                formatted_prompt += f"<s>[INST] {content} [/INST]\n\n"
            elif role == "user":
                if formatted_prompt:
                    formatted_prompt += f"{content} [/INST]\n\n"
                else:
                    formatted_prompt += f"<s>[INST] {content} [/INST]\n\n"
            elif role == "assistant":
                formatted_prompt += f"{content}\n\n"
        
        return formatted_prompt.strip()
    
    def generate_frame_sequence(self, prompt: str, num_frames: int = 5) -> List[FrameDescription]:
        """Generate a sequence of frame descriptions from a prompt."""
        system_message = (
            "You are a creative assistant that converts text prompts into a sequence "
            f"of {num_frames} detailed frame descriptions for a video storyboard. "
            "Each frame should progress the story logically, with clear visual elements. "
            "Focus on showing progression and change across the sequence."
        )
        
        user_message = f"Convert this text into {num_frames} sequential video frames: \"{prompt}\""
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
        
        response = self.call_llm(messages)
        
        # Parse the response into frame descriptions
        frames = []
        try:
            lines = response.strip().split("\n")
            frame_num = 1
            
            for line in lines:
                line = line.strip()
                if line and (line.startswith("Frame") or line.startswith(f"{frame_num}.") or line.startswith(f"{frame_num}:")):
                    # Extract the description part after any numbering or "Frame X:" prefix
                    description = line.split(":", 1)[-1].strip() if ":" in line else line.split(".", 1)[-1].strip()
                    frames.append(FrameDescription(description=description, frame_number=frame_num))
                    frame_num += 1
        except Exception as e:
            # If parsing fails, try a more direct approach
            return self.generate_structured_frame_sequence(prompt, num_frames)
            
        # If we didn't get enough frames, try the structured approach
        if len(frames) < num_frames:
            return self.generate_structured_frame_sequence(prompt, num_frames)
            
        return frames
    
    def generate_structured_frame_sequence(self, prompt: str, num_frames: int = 5) -> List[FrameDescription]:
        """Generate a sequence of frame descriptions with explicit formatting instructions."""
        system_message = (
            "You are a creative assistant that converts text prompts into a sequence "
            f"of {num_frames} detailed frame descriptions for a video storyboard. "
            "Each frame should progress the story logically, with clear visual elements. "
            "\n\nYou MUST format your response exactly as follows, with one frame per line:\n"
            "Frame 1: [description of first frame]\n"
            "Frame 2: [description of second frame]\n"
            "And so on..."
        )
        
        user_message = f"Convert this text into {num_frames} sequential video frames: \"{prompt}\""
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
        
        response = self.call_llm(messages)
        
        # Parse the response into frame descriptions
        frames = []
        
        lines = response.strip().split("\n")
        for i, line in enumerate(lines):
            line = line.strip()
            if line and i < num_frames:
                # Extract the description part after any prefix
                description = line.split(":", 1)[-1].strip() if ":" in line else line
                frames.append(FrameDescription(description=description, frame_number=i+1))
        
        # If we still didn't get enough frames, create generic ones to fill the gap
        while len(frames) < num_frames:
            frame_num = len(frames) + 1
            frames.append(FrameDescription(
                description=f"Continuation of the scene from {prompt}", 
                frame_number=frame_num
            ))
            
        return frames
    
    def refine_frame_sequence(self, frames: List[FrameDescription], prompt: str) -> List[FrameDescription]:
        """Refine a sequence of frame descriptions for linguistic consistency and semantic coherence."""
        
        # Create a formatted list of the current frames
        frames_text = "\n".join([f"Frame {f.frame_number}: {f.description}" for f in frames])
        
        system_message = (
            "You are a detail-oriented editor that refines video frame descriptions to ensure "
            "they maintain linguistic consistency, semantic coherence, and logical progression. "
            "Ensure each frame builds on the previous ones, uses consistent terminology, "
            "and creates a smooth visual narrative."
            "\n\nYou MUST format your response exactly as follows, with one frame per line:\n"
            "Frame 1: [refined description of first frame]\n"
            "Frame 2: [refined description of second frame]\n"
            "And so on..."
        )
        
        user_message = (
            f"Refine these frame descriptions for the prompt: \"{prompt}\"\n\n"
            f"{frames_text}\n\n"
            "Make sure the sequence flows naturally, maintains consistent terminology, "
            "and shows clear progression while preserving the original meaning of each frame."
        )
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
        
        response = self.call_llm(messages)
        
        # Parse the response into refined frame descriptions
        refined_frames = []
        
        lines = response.strip().split("\n")
        for line in lines:
            line = line.strip()
            if line and line.startswith("Frame"):
                parts = line.split(":", 1)
                if len(parts) == 2:
                    try:
                        frame_num = int(parts[0].replace("Frame", "").strip())
                        description = parts[1].strip()
                        refined_frames.append(FrameDescription(
                            description=description, 
                            frame_number=frame_num
                        ))
                    except:
                        # Skip lines that don't conform to the expected format
                        continue
        
        # Ensure the refined frames maintain the same order and count as original frames
        if len(refined_frames) != len(frames):
            # Build a mapping of frame numbers to descriptions
            refined_map = {f.frame_number: f.description for f in refined_frames}
            
            # Create a new list with the same structure as the original frames
            result = []
            for original in frames:
                if original.frame_number in refined_map:
                    result.append(FrameDescription(
                        description=refined_map[original.frame_number],
                        frame_number=original.frame_number
                    ))
                else:
                    # Keep the original if no refinement was provided
                    result.append(original)
            
            refined_frames = result
            
        return refined_frames 