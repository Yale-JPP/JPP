import { BrowserRouter, Routes, Route} from 'react-router-dom';
import './App.css';
import HomePage from './pages/homepage';
import OneTwoNoun from './pages/1+2_noun';

function App() {

  return (

    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage/>}/>
        <Route path="/1+2_noun" element={<OneTwoNoun/>}/>
      </Routes>
    </BrowserRouter>

  )
}

export default App;
