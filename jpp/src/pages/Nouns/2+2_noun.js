import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

function TwoTwoNoun() {
  const [word, setWord] = useState('');
  const [accentType, setAccentType] = useState(0);
  const [audioBlob, setAudioBlob] = useState(null);
  const [grade, setGrade] = useState(null);

  const mimeType = "audio/webm";
  const [stream, setStream] = useState();
  const mediaRecorder = useRef();
  const [permission, setPermission] = useState(false);
  const [chunks, setChunks] = useState([]);
  const [recording, setRecording] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    getUserPermission();
  }, []);

  const getUserPermission = async () => {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      console.log("getUserMedia supported.");
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        setStream(stream);
        setPermission(true);
        console.log(stream);
      } catch (err) {
        console.error(`The following getUserMedia error occurred: ${err}`);
        setError('Error getting user permission: ' + err.message);
      }
    } else {
      console.log("getUserMedia not supported on your browser!");
      setError("getUserMedia not supported on your browser!");
    }
  };

  const handleRecord = () => {
    if (!permission) {
      getUserPermission();
    }

    if (!recording) {
      setRecording(true);
      startRecording();
    } else {
      setRecording(false);
      stopRecording();
    }
  };

  const startRecording = () => {
    const media = new MediaRecorder(stream, { mimeType: mimeType });
    mediaRecorder.current = media;

    mediaRecorder.current.start();
    console.log(mediaRecorder.current.state);
    console.log("recorder started");

    let localChunks = [];

    mediaRecorder.current.ondataavailable = (e) => {
      localChunks.push(e.data);
    };

    setChunks(localChunks);
  };

  const stopRecording = () => {
    mediaRecorder.current.stop();
    console.log(mediaRecorder.current.state);
    console.log("recorder stopped");

    mediaRecorder.current.onstop = (e) => {
      const audioBlob = new Blob(chunks, { type: mimeType });
      setAudioBlob(audioBlob);
    };
  };

  const handleGrade = async () => {
    if (!audioBlob) {
      setError('Please record audio before grading.');
      return;
    }

    const formData = new FormData();
    formData.append('word', word);
    formData.append('accent_type', accentType);
    formData.append('sf', audioBlob, 'recorded_audio.wav');

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
      <button onClick={handleGrade}>Grade</button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {audioBlob && <audio src={URL.createObjectURL(audioBlob)} controls />}
      {grade !== null && <p>Grade: {grade}</p>}
    </div>
  );
}

export default TwoTwoNoun;
