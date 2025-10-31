import React, { useState } from "react";
import ArtGenerator from "./components/ArtGenerator";
import Gallery from "./components/Gallery";
import "./styles.css";

function App() {
  const [artworks, setArtworks] = useState([]);
  const [portfolioName, setPortfolioName] = useState("My AI Art Portfolio");

  const addArtwork = (artwork) => {
    setArtworks([...artworks, artwork]);
  };

  const removeArtwork = (index) => {
    setArtworks(artworks.filter((_, i) => i !== index));
  };

  const exportPortfolio = () => {
    const portfolioData = {
      name: portfolioName,
      created: new Date().toISOString(),
      artworks: artworks
    };
    const dataStr = JSON.stringify(portfolioData, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    
    const exportFileDefaultName = `${portfolioName.replace(/\s+/g, '_')}_${Date.now()}.json`;
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>🎨 AI Portfolio Generator</h1>
        <input
          type="text"
          className="portfolio-name-input"
          value={portfolioName}
          onChange={(e) => setPortfolioName(e.target.value)}
          placeholder="Enter portfolio name"
        />
      </header>
      <ArtGenerator addArtwork={addArtwork} />
      <Gallery 
        artworks={artworks} 
        removeArtwork={removeArtwork}
        exportPortfolio={exportPortfolio}
      />
    </div>
  );
}

export default App;

