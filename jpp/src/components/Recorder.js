import React, { useState, useEffect, useRef } from 'react';
import { Box, Button, InputLabel, MenuItem, Select, TextField } from '@mui/material';
import axios from 'axios';

// Used https://developer.mozilla.org/en-US/docs/Web/API/MediaStream_Recording_API/Using_the_MediaStream_Recording_API
// Assisted by previous code from Murtaza

function Recorder() {
  const [word, setWord] = useState('');
  const [accentType, setAccentType] = useState(0);
  const [reader, setReader] = useState(null);
  const [grade, setGrade] = useState(null);

  const mimeType = "audio/webm";
  const [stream, setStream] = useState();
  const mediaRecorder = useRef();
  const [permission, setPermission] = useState(false);
  const [chunks, setChunks] = useState([]);
  const [recording, setRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState(null);
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

      const reader = new FileReader();
      reader.readAsDataURL(audioBlob);
      setReader(reader);

    };
  };

  const handleGrade = async () => {
    if (!reader) {
      setError('Please record audio before grading.');
      return;
    }

    if (!word) {
      setError('Please enter the word before grading.');
      return;
    }

    const formData = new FormData();
    formData.append('word', word);
    formData.append('accent_type', accentType);
    formData.append('sf', reader.result);

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
    <Box>
      <InputLabel htmlFor="word">Word:</InputLabel>
      <TextField id="word" label="Enter a word" variant="outlined" value={word} onChange={(e) => setWord(e.target.value)}/>
      <InputLabel htmlFor="accentType">Accent Type:</InputLabel>
      <Select id="accentType" value={accentType} onChange={(e) => setAccentType(e.target.value)}>
        <MenuItem value="0">0</MenuItem>
        <MenuItem value="1">1</MenuItem>
        <MenuItem value="2">2</MenuItem>
        <MenuItem value="3">3</MenuItem>
        <MenuItem value="4">4</MenuItem>
      </Select>
      <Button onClick={handleRecord} variant="contained">
        {recording ? 'Stop Recording' : 'Start Recording'}
      </Button>
      <Button onClick={handleGrade} variant="contained">Grade</Button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {audioBlob && <audio src={URL.createObjectURL(audioBlob)} controls />}
      {grade !== null && <p>Grade: {grade}</p>}
    </Box>
  );
}

export default Recorder;
