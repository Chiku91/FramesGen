#!/usr/bin/env python
import argparse
from src import process_prompt

def main():
    """Run the frame description generator."""
    parser = argparse.ArgumentParser(description="Convert a text prompt into a sequence of video frame descriptions")
    parser.add_argument("prompt", type=str, help="The text prompt to convert")
    parser.add_argument("--frames", "-f", type=int, default=5, help="The number of frames to generate (default: 5)")
    
    args = parser.parse_args()
    
    print(f"Processing prompt: {args.prompt}")
    print(f"Generating {args.frames} frames...")
    
    result = process_prompt(args.prompt, args.frames)
    
    print("\n--- Initial Frame Sequence ---")
    for frame in result.frames:
        print(f"Frame {frame.frame_number}: {frame.description}")
    
    print("\n--- Refined Frame Sequence ---")
    for frame in result.refined_frames:
        print(f"Frame {frame.frame_number}: {frame.description}")
    
    print("\nDone!")
    

if __name__ == "__main__":
    main() 