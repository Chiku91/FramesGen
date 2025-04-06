# LLM Serial Prompting for Video Frame Descriptions

This project uses LLM serial prompting to convert a single text prompt into a structured sequence of descriptions for video frames. It demonstrates how to use an LLM (like Mistral or another Hugging Face model) to generate and refine coherent sequences. It can also generate images for each frame description using Stability AI.

## Features

- Convert simple text prompts into detailed frame-by-frame descriptions
- Two-stage prompting process:
  1. Generate initial frame descriptions
  2. Refine descriptions for consistency and coherence
- Generate images for each frame description using Stability AI's API
- Create an HTML visual storyboard overview
- Command-line interface for easy testing

## Example

Input: "A flower is blooming"

Output (Text):
```
Frame 1: A small green bud appears on a slender stem, tightly closed and full of potential.
Frame 2: The bud grows slightly larger, with the first hints of color visible at its tip.
Frame 3: The outer petals begin to loosen and unfurl, revealing the vibrant inner colors.
Frame 4: The flower continues opening, with half its petals now extended outward.
Frame 5: The fully bloomed flower displays all its petals in a radiant pattern, face turned toward the sun.
```

Output (Images):
- Images for each frame saved in the `generated_frames` directory
- Optional HTML storyboard view showing frames with their descriptions

## Setup

1. Clone this repository
2. Install the requirements:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your API keys:
   ```
   HF_API_TOKEN=your_huggingface_token_here
   MODEL_NAME=mistralai/Mistral-7B-Instruct-v0.2  # or another model
   STABILITY_API_KEY=your_stability_api_key_here  # for image generation
   ```

## Getting API Keys

### Hugging Face API Token
1. Create a Hugging Face account at https://huggingface.co/
2. Go to your profile -> Settings -> Access Tokens
3. Create a new token with "read" scope
4. Copy the token to your `.env` file

### Stability API Key (for image generation)
1. Create an account at https://stability.ai/
2. Go to your account dashboard
3. Navigate to API Keys and generate a new key
4. Copy the key to your `.env` file

## Usage

### Generate Frame Descriptions and Images

Run the storyboard generator script with a prompt:

```bash
python generate_storyboard.py "A flower is blooming" --frames 5 --html
```

Options:
- `--frames` or `-f`: Number of frames to generate (default: 5)
- `--style` or `-s`: Style prompt to add to all image generations
- `--negative` or `-n`: Negative prompt for things to avoid in images
- `--skip-images`: Skip image generation and only create frame descriptions
- `--html`: Create an HTML overview file

### Generate Only Frame Descriptions

If you don't have a Stability API key or just want the text descriptions:

```bash
python frame_generator.py "A flower is blooming" --frames 5
```

### Python API

```python
from src import process_prompt, generate_images_for_storyboard

# Generate a sequence of 5 frames
storyboard = process_prompt("A flower is blooming", num_frames=5)

# Access the initial frame descriptions
for frame in storyboard.frames:
    print(f"Frame {frame.frame_number}: {frame.description}")

# Access the refined frame descriptions
for frame in storyboard.refined_frames:
    print(f"Frame {frame.frame_number}: {frame.description}")

# Generate images for the frames
image_paths = generate_images_for_storyboard(storyboard)
```

## How It Works

1. **Initial Frame Generation**: The first LLM call converts the input prompt into a sequence of frame descriptions, each representing a step in the visual progression.

2. **Refinement Process**: The second LLM call takes the initial frame descriptions and refines them to ensure:
   - Linguistic consistency (terminology, style)
   - Semantic coherence (logical progression)
   - Visual continuity (smooth transitions between frames)

3. **Image Generation**: Uses Stability AI's API to convert each frame description into a visual representation, with customizable style guidance.

4. **Storyboard Creation**: Optionally creates an HTML visual storyboard showing all frames with their descriptions.

## Extending the Project

- Add support for more complex prompts with scene transitions
- Create video animations from the still frames
- Create a web interface for interactive use
- Add more refinement steps for specific requirements (style, mood, etc.)
- Try different models from Hugging Face for various capabilities 