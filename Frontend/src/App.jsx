import React, { useState } from 'react';
import axios from 'axios';
import Header from './components/Header';
import Footer from './components/Footer';
import MainContent from './components/MainContent';
import './App.css';

function App() {
  const [prediction, setPrediction] = useState('');
  const [breedInfo, setBreedInfo] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isInfoLoading, setIsInfoLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);

  /**
   * Fetches a description for the predicted dog breed using the Gemini API.
   */
  const fetchBreedInfo = async (breedName) => {
    if (!breedName) return;

    setIsInfoLoading(true);
    setBreedInfo('');
    
    const prompt = `Provide a short, engaging summary (about 50-70 words) for the ${breedName} dog breed. Focus on its temperament, size, and one interesting fact.`;

    try {
        const payload = {
            contents: [{ parts: [{ text: prompt }] }]
        };
        const apiKey = import.meta.env.VITE_GEMINI_API_KEY;
        const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key=${apiKey}`;

        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`API request failed with status ${response.status}`);
        }

        const result = await response.json();
        if (result.candidates && result.candidates[0]?.content?.parts[0]?.text) {
            setBreedInfo(result.candidates[0].content.parts[0].text);
        } else {
            throw new Error("Could not parse breed information from API response.");
        }
    } catch (err) {
        console.error("Error fetching breed info:", err);
        setBreedInfo("Could not retrieve detailed information for this breed.");
    } finally {
        setIsInfoLoading(false);
    }
  };

  /**
   * Handles the prediction process by sending the image to the backend.
   */
  const handlePredict = async () => {
    if (!selectedFile) {
      setError('Please select an image first.');
      return;
    }

    setIsLoading(true);
    setError(null);
    setPrediction('');
    setBreedInfo('');

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await axios.post('http://localhost:8000/predict', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      const breedName = response.data.breed;
      setPrediction(breedName);
      fetchBreedInfo(breedName); // Fetch info for the predicted breed
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'An unexpected error occurred.';
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <Header />
      <MainContent
        selectedFile={selectedFile}
        setSelectedFile={setSelectedFile}
        handlePredict={handlePredict}
        prediction={prediction}
        breedInfo={breedInfo}
        isLoading={isLoading}
        isInfoLoading={isInfoLoading}
        error={error}
      />
      <Footer />
    </div>
  );
}

export default App;