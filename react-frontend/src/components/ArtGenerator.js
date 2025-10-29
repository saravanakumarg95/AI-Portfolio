import React, { useState } from "react";

function ArtGenerator() {
  const [prompt, setPrompt] = useState("");
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);

  const generateArt = async () => {
    if (!prompt.trim()) return;
    setLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:5000/generate", {

        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });
      const data = await response.json();
      setImage(`data:image/png;base64,${data.image}`);
    } catch (err) {
      console.error(err);
      alert("Error generating art!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="generator">
      <h2>🎨 AI Art Generator</h2>
      <input
        type="text"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Describe your artwork..."
      />
      <button onClick={generateArt} disabled={loading}>
        {loading ? "Generating..." : "Generate Art"}
      </button>
      {image && <img src={image} alt="Generated Art" className="art-image" />}
    </div>
  );
}

export default ArtGenerator;
