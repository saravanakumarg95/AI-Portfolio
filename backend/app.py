from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
from diffusers import StableDiffusionPipeline
import base64
from io import BytesIO

# Initialize Flask
app = Flask(__name__)
CORS(app)

# Load Stable Diffusion model (GPU)
print("🔥 Loading Stable Diffusion model on GPU...")
model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to("cuda")
print("✅ Model loaded successfully.")

@app.route("/generate", methods=["POST"])
def generate_art():
    data = request.get_json()
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    print(f"🖌️ Generating image for prompt: {prompt}")

    # Generate image
    image = pipe(prompt).images[0]

    # Convert image to Base64
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return jsonify({"image": image_base64})

if __name__ == "__main__":
    app.run(debug=True)
