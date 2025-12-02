import React from 'react';
import './InfoCard.css';

function InfoCard({ prediction, breedInfo, isLoading, isInfoLoading }) {
  return (
    <div className="card info-card">
      <h2 className="info-title">Breed Information</h2>
      {isLoading ? (
        <div className="placeholder-text">Checking the photo...</div>
      ) : !prediction ? (
        <div className="placeholder-text">
          Upload a photo and click "Identify" to see details here.
        </div>
      ) : (
        <div className="info-content">
          <h3 className="breed-name">{prediction}</h3>
          {isInfoLoading ? (
            <div className="loading-spinner"></div>
          ) : (
            <p className="breed-description">{breedInfo}</p>
          )}
        </div>
      )}
    </div>
  );
}

export default InfoCard;