import React from 'react';
import './ImageUpload.css';

function ImageUpload({ onFileSelect, imagePreview }) {
  return (
    <div className="image-upload-container">
      <label htmlFor="file-upload" className="file-upload-label">
        {imagePreview ? (
          <img src={imagePreview} alt="Dog preview" className="image-preview" />
        ) : (
          <div className="upload-placeholder">
            <span>🖼️</span>
            <p>Click to select an image</p>
          </div>
        )}
      </label>
      <input
        id="file-upload"
        type="file"
        accept="image/*"
        onChange={onFileSelect}
        className="file-input"
      />
    </div>
  );
}

export default ImageUpload;