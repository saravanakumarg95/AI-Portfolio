import React, { useState } from "react";
import ArtGenerator from "./components/ArtGenerator";
import Gallery from "./components/Gallery";
import "./styles.css";

function App() {
  const [artworks, setArtworks] = useState([]);

  const addArtwork = (image) => setArtworks([...artworks, image]);

  return (
    <div className="app">
      <h1>🎨 AI Art Portfolio</h1>
      <ArtGenerator addArtwork={addArtwork} />
      <Gallery artworks={artworks} />
    </div>
  );
}

export default App;

