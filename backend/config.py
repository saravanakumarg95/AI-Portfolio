# Model Configuration for Enhanced Quality

# Model Settings
MODEL_ID = "runwayml/stable-diffusion-v1-5"
# Alternative high-quality models (uncomment to use):
# MODEL_ID = "stabilityai/stable-diffusion-2-1"
# MODEL_ID = "prompthero/openjourney-v4"

# Generation Parameters (defaults)
DEFAULT_INFERENCE_STEPS = 50  # Higher = better quality but slower (range: 20-150)
DEFAULT_GUIDANCE_SCALE = 7.5  # Higher = follows prompt more closely (range: 5-15)
DEFAULT_WIDTH = 512
DEFAULT_HEIGHT = 512

# Quality Enhancement
NEGATIVE_PROMPT_DEFAULT = (
    "blurry, bad quality, distorted, ugly, low resolution, "
    "pixelated, disfigured, deformed, mutated, amateur, "
    "watermark, text, signature"
)

# Performance Settings
ENABLE_ATTENTION_SLICING = True  # Reduces memory usage
ENABLE_VAE_SLICING = True  # Further memory optimization
USE_FP16 = True  # Half precision for faster generation

# Prompt Enhancement Keywords
QUALITY_KEYWORDS = [
    "highly detailed",
    "professional quality",
    "8k resolution",
    "masterpiece",
    "sharp focus",
    "trending on artstation",
    "award-winning",
    "photorealistic"
]

ARTISTIC_KEYWORDS = [
    "digital art",
    "concept art",
    "illustration",
    "cinematic lighting",
    "vibrant colors",
    "dramatic composition"
]
