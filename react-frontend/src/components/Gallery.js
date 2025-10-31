import React, { useState } from "react";

function Gallery({ artworks, removeArtwork, exportPortfolio }) {
  const [selectedArt, setSelectedArt] = useState(null);

  const openModal = (artwork, index) => {
    setSelectedArt({ ...artwork, index });
  };

  const closeModal = () => {
    setSelectedArt(null);
  };

  const downloadArtwork = (artwork) => {
    const link = document.createElement('a');
    link.href = artwork.image;
    link.download = `artwork_${Date.now()}.png`;
    link.click();
  };

  return (
    <div className="gallery">
      <div className="gallery-header">
        <h2>🖼️ Your Art Gallery ({artworks.length} artworks)</h2>
        {artworks.length > 0 && (
          <button onClick={exportPortfolio} className="export-btn">
            📦 Export Portfolio
          </button>
        )}
      </div>

      {artworks.length === 0 ? (
        <div className="empty-gallery">
          <p>🎨 Your gallery is empty. Start creating art!</p>
        </div>
      ) : (
        <div className="gallery-grid">
          {artworks.map((artwork, index) => (
            <div key={index} className="gallery-item">
              <img 
                src={artwork.image} 
                alt={`Art ${index}`}
                onClick={() => openModal(artwork, index)}
              />
              <div className="gallery-item-overlay">
                <button 
                  onClick={(e) => {
                    e.stopPropagation();
                    removeArtwork(index);
                  }}
                  className="remove-btn"
                  title="Remove from gallery"
                >
                  🗑️
                </button>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    downloadArtwork(artwork);
                  }}
                  className="download-btn-small"
                  title="Download"
                >
                  💾
                </button>
              </div>
              <div className="gallery-item-info">
                <p className="prompt-preview">{artwork.prompt.substring(0, 50)}...</p>
              </div>
            </div>
          ))}
        </div>
      )}

      {selectedArt && (
        <div className="modal" onClick={closeModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <span className="close" onClick={closeModal}>&times;</span>
            <img src={selectedArt.image} alt="Selected Art" className="modal-image" />
            <div className="modal-details">
              <h3>Artwork Details</h3>
              <p><strong>Prompt:</strong> {selectedArt.prompt}</p>
              {selectedArt.negativePrompt && (
                <p><strong>Negative Prompt:</strong> {selectedArt.negativePrompt}</p>
              )}
              {selectedArt.settings && (
                <p><strong>Settings:</strong> {selectedArt.settings.steps} steps, 
                   guidance {selectedArt.settings.guidance_scale}, 
                   {selectedArt.settings.dimensions}</p>
              )}
              <p><strong>Created:</strong> {new Date(selectedArt.timestamp).toLocaleString()}</p>
              <div className="modal-actions">
                <button onClick={() => downloadArtwork(selectedArt)} className="modal-btn">
                  💾 Download
                </button>
                <button 
                  onClick={() => {
                    removeArtwork(selectedArt.index);
                    closeModal();
                  }} 
                  className="modal-btn remove"
                >
                  🗑️ Remove
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Gallery;
