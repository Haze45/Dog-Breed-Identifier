import React, { useState } from 'react';
import ImageUpload from './ImageUpload';
import './UploadCard.css';

function UploadCard({ setSelectedFile, handlePredict, isLoading, error }) {
  const [imagePreview, setImagePreview] = useState('');

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setImagePreview(URL.createObjectURL(file));
    }
  };

  return (
    <div className="card upload-card">
      <ImageUpload onFileSelect={handleFileSelect} imagePreview={imagePreview} />
      <button
        onClick={handlePredict}
        className="predict-button"
        disabled={!imagePreview || isLoading}
      >
        {isLoading ? 'Identifying...' : 'Identify Breed'}
      </button>
      {error && <div className="error-message">{error}</div>}
    </div>
  );
}

export default UploadCard;