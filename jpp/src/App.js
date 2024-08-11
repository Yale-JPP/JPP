import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './App.css';
import HomePage from './pages/Homepage';
import Nouns from './pages/Nouns/Nouns';
import OneTwoNoun from './pages/Nouns/1+2_noun';
import TwoOneNoun from './pages/Nouns/2+1_noun';
import TwoTwoNoun from './pages/Nouns/2+2_noun';
import ChineseOriginated from './pages/Nouns/Chinese_Originated';
import Gairaigo from './pages/Nouns/Gairaigo';
import Compound from './pages/Nouns/Compound';
import Dictionary from './pages/Verbs/Dictionary';
import Masu from './pages/Verbs/Masu';
import NegativeDict from './pages/Verbs/Negative_Dict';
import TeTaForm from './pages/Verbs/Te_Ta';
import Verbs from './pages/Verbs/Verbs';
import Names from './pages/Names';
import GenericPitchTips from './pages/GenericPitchTips';
// import { Nouns, OneTwoNoun, TwoOneNoun, TwoTwoNoun, ChineseOriginated, Gairaigo } from './pages/Nouns/';
import Navbar from './components/Navbar'
import { Box } from '@mui/material';

function App() {

  return (
    
    <BrowserRouter>
      <Box>
        <Navbar/>
        <Routes>
          <Route path="/" element={<HomePage/>}/>
          {/* Nouns */}
          <Route path="/nouns" element={<Nouns/>}/>
          <Route path="/1+2-Nouns" element={<OneTwoNoun/>}/>
          <Route path="/2+1-Nouns" element={<TwoOneNoun/>}/>
          <Route path="/2+2-Nouns" element={<TwoTwoNoun/>}/>
          <Route path="/chinese-originated" element={<ChineseOriginated/>}/>
          <Route path="/compounds" element={<Compound/>}/>
          <Route path="/gairaigo" element={<Gairaigo/>}/>
          {/* Verbs */}
          <Route path="/verbs" element={<Verbs/>}/>
          <Route path="/dictionary" element={<Dictionary/>}/>
          <Route path="/masu-form" element={<Masu/>}/>
          <Route path="/negatives" element={<NegativeDict/>}/>
          <Route path="/te-ta" element={<TeTaForm/>}/>
          {/* Names */}
          <Route path="/names" element={<Names/>}/>
          {/* Generic */}
          <Route path="/generic-pitch-tips" element={<GenericPitchTips/>}/>
        </Routes>
      </Box>
    </BrowserRouter>

  )
}

export default App;