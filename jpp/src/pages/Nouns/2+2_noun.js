import React, { useState } from 'react';
import axios from 'axios';

function TwoTwoNoun() {
  const [word, setWord] = useState('');
  const [accentType, setAccentType] = useState(0);
  const [audioBlob, setAudioBlob] = useState(null);
  const [recording, setRecording] = useState(false);
  const [grade, setGrade] = useState(null);
  const [error, setError] = useState(null);

  const handleRecord = async () => {
    if (!recording) {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      const audioChunks = [];

      mediaRecorder.addEventListener('dataavailable', event => {
        audioChunks.push(event.data);
      });

      mediaRecorder.addEventListener('stop', () => {
        const audioBlob = new Blob(audioChunks);
        setAudioBlob(audioBlob);
      });

      mediaRecorder.start();
      setRecording(true);
    } else {
      setRecording(false);
    }
  };

  const handlePlayback = () => {
    // if (!audioBlob) {
    //   setError('Please record audio before playback.');
    //   return;
    // }

    const audioURL = URL.createObjectURL(audioBlob);
    const audio = new Audio(audioURL);
    audio.play();
  };

  const handleGrade = async () => {
    // if (!audioBlob) {
    //   setError('Please record audio before grading.');
    //   return;
    // }

    const formData = new FormData();
    formData.append('word', word);
    formData.append('accent_type', accentType);
    formData.append('sf', audioBlob);

    try {
      const response = await axios.post('/grade', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      const { grade } = response.data;
      setGrade(grade);
    } catch (error) {
      console.error('Error grading:', error);
    }
  };

  return (
    <div>
      <label htmlFor="word">Word:</label>
      <input
        type="text"
        id="word"
        value={word}
        onChange={(e) => setWord(e.target.value)}
        placeholder="Enter a word"
      />
      <label htmlFor="accentType">Accent Type:</label>
      <select id="accentType" value={accentType} onChange={(e) => setAccentType(e.target.value)}>
        <option value="0">0</option>
        <option value="1">1</option>
        <option value="2">2</option>
        <option value="3">3</option>
        <option value="4">4</option>
      </select>
      <button onClick={handleRecord}>
        {recording ? 'Stop Recording' : 'Start Recording'}
      </button>
      <button onClick={handlePlayback}>Playback</button>
      <button onClick={handleGrade}>Grade</button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {grade !== null && <p>Grade: {grade}</p>}
    </div>
  );
}

export default TwoTwoNoun;
