from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
import base64
from io import BytesIO
import config

# Initialize Flask
app = Flask(__name__)
CORS(app)

# Load Stable Diffusion model with optimizations
print("🔥 Loading Stable Diffusion model on GPU...")
pipe = StableDiffusionPipeline.from_pretrained(
    config.MODEL_ID, 
    torch_dtype=torch.float16 if config.USE_FP16 else torch.float32,
    safety_checker=None,  # Remove for faster generation
    requires_safety_checker=False
)

# Use DPM-Solver++ for faster and better quality generation
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)

# Move to GPU and enable memory optimizations
pipe = pipe.to("cuda")
if config.ENABLE_ATTENTION_SLICING:
    pipe.enable_attention_slicing()  # Reduce memory usage
if config.ENABLE_VAE_SLICING:
    pipe.enable_vae_slicing()  # Further memory optimization

print("✅ Model loaded successfully with optimizations.")

@app.route("/generate", methods=["POST"])
def generate_art():
    data = request.get_json()
    prompt = data.get("prompt", "")
    negative_prompt = data.get("negative_prompt", config.NEGATIVE_PROMPT_DEFAULT)
    num_inference_steps = data.get("steps", config.DEFAULT_INFERENCE_STEPS)
    guidance_scale = data.get("guidance_scale", config.DEFAULT_GUIDANCE_SCALE)
    width = data.get("width", config.DEFAULT_WIDTH)
    height = data.get("height", config.DEFAULT_HEIGHT)
    seed = data.get("seed", None)

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    print(f"🖌️ Generating image for prompt: {prompt}")
    print(f"⚙️ Settings: steps={num_inference_steps}, guidance={guidance_scale}, size={width}x{height}")

    # Set seed for reproducibility if provided
    generator = None
    if seed is not None:
        generator = torch.Generator(device="cuda").manual_seed(seed)

    # Generate image with enhanced parameters
    try:
        output = pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            width=width,
            height=height,
            generator=generator
        )
        image = output.images[0]

        # Convert image to Base64
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return jsonify({
            "image": image_base64,
            "seed": seed if seed is not None else "random",
            "settings": {
                "steps": num_inference_steps,
                "guidance_scale": guidance_scale,
                "dimensions": f"{width}x{height}"
            }
        })
    except Exception as e:
        print(f"❌ Error generating image: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint to verify the API is running"""
    return jsonify({
        "status": "healthy",
        "model": "stable-diffusion-v1-5",
        "device": "cuda" if torch.cuda.is_available() else "cpu"
    })

@app.route("/enhance-prompt", methods=["POST"])
def enhance_prompt():
    """Enhance user prompt with better keywords for higher quality generation"""
    data = request.get_json()
    user_prompt = data.get("prompt", "")
    
    if not user_prompt:
        return jsonify({"error": "Prompt is required"}), 400
    
    # Add quality enhancers to the prompt
    enhanced = f"{user_prompt}, highly detailed, professional quality, 8k resolution, masterpiece, trending on artstation"
    
    return jsonify({
        "original": user_prompt,
        "enhanced": enhanced
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
