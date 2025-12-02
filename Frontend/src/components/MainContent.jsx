import React from 'react';
import UploadCard from './UploadCard';
import InfoCard from './InfoCard';
import './MainContent.css';

function MainContent({
  selectedFile,
  setSelectedFile,
  handlePredict,
  prediction,
  breedInfo,
  isLoading,
  isInfoLoading,
  error,
}) {
  return (
    <main className="app-main">
      <UploadCard
        selectedFile={selectedFile}
        setSelectedFile={setSelectedFile}
        handlePredict={handlePredict}
        isLoading={isLoading}
        error={error}
      />
      <InfoCard
        prediction={prediction}
        breedInfo={breedInfo}
        isLoading={isLoading}
        isInfoLoading={isInfoLoading}
      />
    </main>
  );
}

export default MainContent;