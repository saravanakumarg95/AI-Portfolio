import React from "react";

function Gallery({ artworks }) {
  return (
    <div className="gallery">
      <h2>🖼️ Your Art Gallery</h2>
      <div className="gallery-grid">
        {artworks.map((art, index) => (
          <img key={index} src={art} alt={`Art ${index}`} />
        ))}
      </div>
    </div>
  );
}

export default Gallery;
