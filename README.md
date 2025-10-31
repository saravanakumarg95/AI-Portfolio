# 🎨 AI Portfolio Generator

A professional AI-powered portfolio generation system using Stable Diffusion with enhanced model accuracy and quality optimization.

## ✨ Features

### 🚀 Enhanced Model Accuracy
- **Advanced Scheduler**: Uses DPM-Solver++ for 2-3x faster generation with better quality
- **Optimized Parameters**: Fine-tuned inference steps (50 default) and guidance scale (7.5)
- **Negative Prompts**: Automatic filtering of unwanted elements
- **Memory Optimization**: Attention slicing and VAE slicing for efficient GPU usage
- **FP16 Precision**: Half-precision for faster generation without quality loss

### 🎯 Portfolio Features
- **Smart Prompt Enhancement**: Auto-enhance prompts with quality keywords
- **Preset Templates**: Quick-start templates for common use cases
- **Advanced Controls**: 
  - Inference steps (20-150)
  - Guidance scale (5-15)
  - Multiple dimensions (512x512, 768x512, 512x768, 768x768)
  - Seed control for reproducibility
- **Gallery Management**: 
  - View, download, and organize generated artworks
  - Export entire portfolio as JSON
  - Detailed metadata for each artwork
- **Professional UI**: Modern, responsive design with dark theme

## 🛠️ Installation

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure settings in `config.py`:
- Adjust `DEFAULT_INFERENCE_STEPS` for quality vs speed trade-off
- Modify `DEFAULT_GUIDANCE_SCALE` for prompt adherence
- Change `MODEL_ID` to use different Stable Diffusion models

5. Run the backend:
```bash
python app.py
```

Backend will run on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd react-frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

Frontend will run on `http://localhost:3000`

## 📊 Model Accuracy Improvements

### 1. **DPM-Solver++ Scheduler**
- Reduces sampling steps needed by 50-70%
- Maintains or improves output quality
- Faster convergence to high-quality results

### 2. **Optimized Default Parameters**
```python
DEFAULT_INFERENCE_STEPS = 50  # Sweet spot for quality/speed
DEFAULT_GUIDANCE_SCALE = 7.5  # Balanced prompt following
```

### 3. **Comprehensive Negative Prompts**
Automatically filters out:
- Blurry or low-quality outputs
- Distorted or disfigured elements
- Unwanted artifacts
- Watermarks and text

### 4. **Quality Enhancement Keywords**
Auto-adds professional keywords:
- "highly detailed"
- "professional quality"
- "8k resolution"
- "masterpiece"
- "sharp focus"

## 🎯 API Endpoints

### POST `/generate`
Generate artwork from text prompt

**Request:**
```json
{
  "prompt": "A beautiful sunset over mountains",
  "negative_prompt": "blurry, distorted",
  "steps": 50,
  "guidance_scale": 7.5,
  "width": 512,
  "height": 512,
  "seed": 42
}
```

**Response:**
```json
{
  "image": "base64_encoded_image",
  "seed": 42,
  "settings": {
    "steps": 50,
    "guidance_scale": 7.5,
    "dimensions": "512x512"
  }
}
```

### POST `/enhance-prompt`
Enhance user prompt with quality keywords

**Request:**
```json
{
  "prompt": "A portrait of a woman"
}
```

**Response:**
```json
{
  "original": "A portrait of a woman",
  "enhanced": "A portrait of a woman, highly detailed, professional quality, 8k resolution, masterpiece, trending on artstation"
}
```

### GET `/health`
Check API health status

**Response:**
```json
{
  "status": "healthy",
  "model": "stable-diffusion-v1-5",
  "device": "cuda"
}
```

## ⚙️ Configuration Guide

### Quality vs Speed Trade-offs

| Setting | Quality | Speed | Recommendation |
|---------|---------|-------|----------------|
| Steps: 20-30 | Low | Fast | Quick previews |
| Steps: 40-60 | Good | Medium | **Recommended** |
| Steps: 70-100 | High | Slow | Final artworks |
| Steps: 100+ | Very High | Very Slow | Professional use |

### Guidance Scale Guidelines

| Scale | Effect | Use Case |
|-------|--------|----------|
| 5-7 | More creative, loose interpretation | Artistic freedom |
| 7-9 | **Balanced** | General use |
| 9-12 | Strict prompt following | Precise requirements |
| 12+ | Very strict, may reduce quality | Avoid unless needed |

## 🎨 Usage Tips

### For Best Results:

1. **Be Descriptive**: Include details about style, lighting, mood
   ```
   ❌ "A cat"
   ✅ "A fluffy persian cat sitting on a windowsill, soft natural lighting, professional photography"
   ```

2. **Use Negative Prompts**: Specify what you don't want
   ```
   "blurry, distorted, ugly, low quality, amateur"
   ```

3. **Leverage Presets**: Start with templates and customize

4. **Experiment with Seeds**: Use same seed for variations

5. **Adjust Guidance**: Higher for literal interpretation, lower for creativity

## 🔧 Troubleshooting

### CUDA Out of Memory
- Reduce image dimensions to 512x512
- Enable attention slicing (already enabled by default)
- Lower batch size if generating multiple images

### Slow Generation
- Reduce inference steps to 30-40
- Use smaller image dimensions
- Check GPU is being used (not CPU)

### Low Quality Output
- Increase inference steps to 60-75
- Add quality keywords to prompt
- Use negative prompts effectively
- Increase guidance scale to 8-9

## 📦 Project Structure

```
ai-portfolio/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── config.py              # Configuration settings
│   └── requirements.txt       # Python dependencies
├── react-frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ArtGenerator.js   # Generation interface
│   │   │   └── Gallery.js        # Portfolio gallery
│   │   ├── App.js             # Main React component
│   │   └── styles.css         # Styling
│   └── package.json           # Node dependencies
└── README.md
```

## 🚀 Future Enhancements

- [ ] Support for multiple Stable Diffusion models
- [ ] Image-to-image generation
- [ ] Inpainting capabilities
- [ ] ControlNet integration
- [ ] Batch generation
- [ ] Cloud storage integration
- [ ] Social sharing features
- [ ] AI-powered prompt suggestions

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 👏 Acknowledgments

- Stable Diffusion by Stability AI
- Hugging Face Diffusers library
- React community

---

**Made with ❤️ using Stable Diffusion**
