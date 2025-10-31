import React, { useState } from "react";

function ArtGenerator({ addArtwork }) {
  const [prompt, setPrompt] = useState("");
  const [negativePrompt, setNegativePrompt] = useState("");
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [enhancePrompt, setEnhancePrompt] = useState(true);
  const [advancedSettings, setAdvancedSettings] = useState(false);
  const [settings, setSettings] = useState({
    steps: 50,
    guidance_scale: 7.5,
    width: 512,
    height: 512,
    seed: null
  });
  const [generationInfo, setGenerationInfo] = useState(null);

  const presetPrompts = [
    "Professional headshot portrait, studio lighting, business attire",
    "Modern minimalist logo design, clean lines, vector art",
    "Landscape photography, golden hour, mountains and lake",
    "Abstract digital art, vibrant colors, geometric patterns",
    "Character concept art, fantasy warrior, detailed armor",
    "Product photography, white background, professional lighting"
  ];

  const enhanceUserPrompt = async () => {
    if (!prompt.trim()) return prompt;
    
    try {
      const response = await fetch("http://127.0.0.1:5000/enhance-prompt", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });
      const data = await response.json();
      return data.enhanced;
    } catch (err) {
      console.error("Failed to enhance prompt:", err);
      return prompt;
    }
  };

  const generateArt = async () => {
    if (!prompt.trim()) {
      alert("Please enter a prompt!");
      return;
    }
    
    setLoading(true);
    setGenerationInfo(null);
    
    try {
      const finalPrompt = enhancePrompt ? await enhanceUserPrompt() : prompt;
      
      const requestBody = {
        prompt: finalPrompt,
        negative_prompt: negativePrompt || undefined,
        steps: settings.steps,
        guidance_scale: settings.guidance_scale,
        width: settings.width,
        height: settings.height,
        seed: settings.seed || undefined
      };

      const response = await fetch("http://127.0.0.1:5000/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      const imageData = `data:image/png;base64,${data.image}`;
      setImage(imageData);
      setGenerationInfo(data.settings);
    } catch (err) {
      console.error("Generation error:", err);
      alert("Error generating art! Make sure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const addToGallery = () => {
    if (image) {
      const artworkData = {
        image: image,
        prompt: prompt,
        negativePrompt: negativePrompt,
        settings: generationInfo,
        timestamp: new Date().toISOString()
      };
      addArtwork(artworkData);
      alert("Added to gallery!");
    }
  };

  const downloadImage = () => {
    if (image) {
      const link = document.createElement('a');
      link.href = image;
      link.download = `artwork_${Date.now()}.png`;
      link.click();
    }
  };

  return (
    <div className="generator">
      <h2>🎨 AI Art Generator</h2>
      
      <div className="preset-prompts">
        <label>Quick Templates:</label>
        <select onChange={(e) => setPrompt(e.target.value)} value="">
          <option value="">Select a template...</option>
          {presetPrompts.map((preset, idx) => (
            <option key={idx} value={preset}>{preset}</option>
          ))}
        </select>
      </div>

      <div className="prompt-section">
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Describe your artwork in detail..."
          rows="3"
          className="prompt-input"
        />
        
        <div className="prompt-options">
          <label>
            <input
              type="checkbox"
              checked={enhancePrompt}
              onChange={(e) => setEnhancePrompt(e.target.checked)}
            />
            Auto-enhance prompt for better quality
          </label>
        </div>

        <textarea
          value={negativePrompt}
          onChange={(e) => setNegativePrompt(e.target.value)}
          placeholder="Negative prompt (what to avoid)..."
          rows="2"
          className="negative-prompt-input"
        />
      </div>

      <div className="settings-toggle">
        <button 
          onClick={() => setAdvancedSettings(!advancedSettings)}
          className="toggle-btn"
        >
          {advancedSettings ? "Hide" : "Show"} Advanced Settings
        </button>
      </div>

      {advancedSettings && (
        <div className="advanced-settings">
          <div className="setting-group">
            <label>
              Inference Steps: {settings.steps}
              <input
                type="range"
                min="20"
                max="150"
                value={settings.steps}
                onChange={(e) => setSettings({...settings, steps: parseInt(e.target.value)})}
              />
              <span className="setting-hint">Higher = Better quality, slower</span>
            </label>
          </div>

          <div className="setting-group">
            <label>
              Guidance Scale: {settings.guidance_scale}
              <input
                type="range"
                min="5"
                max="15"
                step="0.5"
                value={settings.guidance_scale}
                onChange={(e) => setSettings({...settings, guidance_scale: parseFloat(e.target.value)})}
              />
              <span className="setting-hint">Higher = Follows prompt more closely</span>
            </label>
          </div>

          <div className="setting-group">
            <label>
              Dimensions:
              <select 
                value={`${settings.width}x${settings.height}`}
                onChange={(e) => {
                  const [w, h] = e.target.value.split('x').map(Number);
                  setSettings({...settings, width: w, height: h});
                }}
              >
                <option value="512x512">Square (512x512)</option>
                <option value="768x512">Landscape (768x512)</option>
                <option value="512x768">Portrait (512x768)</option>
                <option value="768x768">Large Square (768x768)</option>
              </select>
            </label>
          </div>

          <div className="setting-group">
            <label>
              Seed (for reproducibility):
              <input
                type="number"
                value={settings.seed || ''}
                onChange={(e) => setSettings({...settings, seed: e.target.value ? parseInt(e.target.value) : null})}
                placeholder="Random"
              />
            </label>
          </div>
        </div>
      )}

      <button 
        onClick={generateArt} 
        disabled={loading}
        className="generate-btn"
      >
        {loading ? "🎨 Generating..." : "✨ Generate Art"}
      </button>

      {image && (
        <div className="result-section">
          <img src={image} alt="Generated Art" className="art-image" />
          
          {generationInfo && (
            <div className="generation-info">
              <p><strong>Settings:</strong> {generationInfo.steps} steps, guidance {generationInfo.guidance_scale}, {generationInfo.dimensions}</p>
            </div>
          )}

          <div className="action-buttons">
            <button onClick={addToGallery} className="add-btn">
              📁 Add to Gallery
            </button>
            <button onClick={downloadImage} className="download-btn">
              💾 Download
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default ArtGenerator;
