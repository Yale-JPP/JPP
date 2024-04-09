import './App.css';
import { Button } from '@mui/material';
import { useState, useRef } from 'react';

function App() {

  const [stream, setStream] = useState();
  const mediaRecorder = useRef();
  const [permission, setPermission] = useState(false);
  const [chunks, setChunks] = useState([]);
  // const [audio, setAudio] = useState("");

  const getUserPermission = async () => {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      console.log("getUserMedia supported.");
      navigator.mediaDevices
        .getUserMedia(
          // constraints - only audio needed for this app
          {
            audio: true,
          },
        )
  
        // Success callback
        .then((stream) => {
          setStream(stream)
          setPermission(true)
          console.log(stream)
        })
  
        // Error callback
        .catch((err) => {
          console.error(`The following getUserMedia error occurred: ${err}`);
        });
    } else {
      console.log("getUserMedia not supported on your browser!");
    }
  }

  const startRecording = () => {
    const media = new MediaRecorder(stream);

    mediaRecorder.current = media;

    mediaRecorder.current.start();
    console.log(mediaRecorder.current.state);
    console.log("recorder started");
    
    let localChunks = [];

    mediaRecorder.current.ondataavailable = (e) => {
      localChunks.push(e.data);
    };

    setChunks(localChunks)

  }

  const stopRecording = () => {
    mediaRecorder.current.stop();
    console.log(mediaRecorder.current.state);
    // console.log("recorder stopped");

    mediaRecorder.current.onstop = (e) => {
      console.log("recorder stopped");
    
      const blob = new Blob(chunks, { type: "audio/ogg; codecs=opus" });
      const audioURL = window.URL.createObjectURL(blob);
      // setAudio(audioURL);
      // audio.src = audioURL

      document.getElementById("audio").src=audioURL;

      console.log(audioURL)
    };
    
  }

  const recordClick = async () => {
    if (!permission) {
      getUserPermission();
    }
    else {
      startRecording();
    } 
    
  }

  return (
    <div className="App">
      <Button variant="contained" onClick={recordClick}>Record</Button>
      <Button variant="contained" onClick={stopRecording}>Stop</Button>
      <audio id='audio' controls></audio>
      {/* <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header> */}
    </div>
  );
}

export default App;
