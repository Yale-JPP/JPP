import './App.css';
import { Button } from '@mui/material';
import { useState, useRef, useEffect } from 'react';

// Used https://developer.mozilla.org/en-US/docs/Web/API/MediaStream_Recording_API/Using_the_MediaStream_Recording_API
// Assisted by previous code from Murtaza

function App() {
  const mimeType = "audio/webm";
  const [stream, setStream] = useState();
  const mediaRecorder = useRef();
  const [permission, setPermission] = useState(false);
  const [chunks, setChunks] = useState([]);
  // const [audio, setAudio] = useState("");

  useEffect(() => {
    getUserPermission();
  }, []);

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
    const media = new MediaRecorder(stream, { mimeType: mimeType });

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
    console.log("recorder stopped");

    mediaRecorder.current.onstop = (e) => {
      const audioBlob = new Blob(chunks, { type: mimeType });

      const reader = new FileReader();

      reader.addEventListener("loadend", async () => {
        // reader.result contains the contents of blob as a typed array
        console.log(reader.result);
        const response = await fetch('/parse-syllables', {
          method: 'POST',
          headers: {
            "Content-Type": "application/json" 
          },
          body: JSON.stringify({
            "audio": reader.result
          })
        });
        const result = await response.json();
        console.log(result);
      });
      reader.readAsDataURL(audioBlob);
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
    </div>
  );
}

export default App;
