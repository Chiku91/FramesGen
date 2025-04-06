#!/usr/bin/env python
import argparse
import os
from PIL import Image
import shutil
from src import process_prompt, generate_images_for_storyboard

def main():
    """Generate a visual storyboard from a text prompt."""
    parser = argparse.ArgumentParser(description="Generate a visual storyboard from a text prompt")
    parser.add_argument("prompt", type=str, help="The text prompt to convert")
    parser.add_argument("--frames", "-f", type=int, default=5, help="The number of frames to generate (default: 5)")
    parser.add_argument("--style", "-s", type=str, default="high quality, detailed, cinematic lighting", 
                        help="Style prompt to add to all image generations")
    parser.add_argument("--negative", "-n", type=str, default="blurry, low quality, distorted, deformed", 
                        help="Negative prompt for things to avoid in images")
    parser.add_argument("--skip-images", action="store_true", help="Skip image generation and only create frame descriptions")
    parser.add_argument("--html", action="store_true", help="Create an HTML overview file")
    
    args = parser.parse_args()
    
    print(f"Processing prompt: {args.prompt}")
    
    # Step 1: Generate frame descriptions
    print(f"Generating {args.frames} frame descriptions...")
    result = process_prompt(args.prompt, args.frames)
    
    # Print the results
    print("\n--- Initial Frame Sequence ---")
    for frame in result.frames:
        print(f"Frame {frame.frame_number}: {frame.description}")
    
    print("\n--- Refined Frame Sequence ---")
    for frame in result.refined_frames:
        print(f"Frame {frame.frame_number}: {frame.description}")
    
    # Step 2: Generate images if not skipped
    image_paths = []
    if not args.skip_images:
        print("\n--- Generating Images ---")
        image_paths = generate_images_for_storyboard(
            result, 
            style_prompt=args.style,
            negative_prompt=args.negative
        )
        
        if image_paths:
            print(f"\nGenerated {len(image_paths)} images in the 'generated_frames' directory")
        else:
            print("\nNo images were generated. Check if your Stability API key is valid.")
    
    # Step 3: Create HTML overview if requested
    if args.html and image_paths:
        create_html_overview(result, image_paths)
    
    print("\nDone!")
    

def create_html_overview(storyboard, image_paths):
    """Create an HTML file showing the storyboard with images and descriptions."""
    output_dir = os.path.join(os.getcwd(), "generated_frames")
    html_path = os.path.join(output_dir, "storyboard_overview.html")
    
    # Copy all images to ensure they're in the same directory as the HTML
    for image_path in image_paths:
        if os.path.exists(image_path):
            filename = os.path.basename(image_path)
            if not os.path.exists(os.path.join(output_dir, filename)):
                shutil.copy(image_path, output_dir)
    
    # Create the HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Storyboard: {storyboard.prompt}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1 {{ color: #333; }}
            .storyboard {{ display: flex; flex-wrap: wrap; gap: 20px; }}
            .frame {{ 
                width: 300px;
                border: 1px solid #ddd;
                padding: 10px;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }}
            .frame img {{ width: 100%; height: auto; border-radius: 5px; }}
            .frame-number {{ font-weight: bold; margin: 10px 0 5px; }}
            .description {{ color: #555; }}
        </style>
    </head>
    <body>
        <h1>Storyboard: {storyboard.prompt}</h1>
        <div class="storyboard">
    """
    
    # Add each frame to the HTML
    for i, frame in enumerate(storyboard.refined_frames):
        if i < len(image_paths):
            image_filename = os.path.basename(image_paths[i])
            html_content += f"""
            <div class="frame">
                <img src="{image_filename}" alt="Frame {frame.frame_number}">
                <p class="frame-number">Frame {frame.frame_number}</p>
                <p class="description">{frame.description}</p>
            </div>
            """
    
    html_content += """
        </div>
    </body>
    </html>
    """
    
    # Write the HTML file
    with open(html_path, "w") as f:
        f.write(html_content)
    
    print(f"Created HTML overview: {html_path}")


if __name__ == "__main__":
    main() 