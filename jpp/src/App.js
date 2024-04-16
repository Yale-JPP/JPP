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

function App() {

  return (

    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage/>}/>

        <Route path="/nouns" element={<Nouns/>}/>
        <Route path="/1+2_noun" element={<OneTwoNoun/>}/>
        <Route path="/2+1_noun" element={<TwoOneNoun/>}/>
        <Route path="/2+2_noun" element={<TwoTwoNoun/>}/>
        <Route path="/chinese_originated" element={<ChineseOriginated/>}/>
        <Route path="/compound" element={<Compound/>}/>
        <Route path="/gairaigo" element={<Gairaigo/>}/>

        <Route path="/verbs" element={<Verbs/>}/>
        <Route path="/dictionary" element={<Dictionary/>}/>
        <Route path="/masu_form" element={<Masu/>}/>
        <Route path="/negative_dict" element={<NegativeDict/>}/>
        <Route path="/te_ta" element={<TeTaForm/>}/>

        <Route path="/names" element={<Names/>}/>

        <Route path="/generic_pitch_tips" element={<GenericPitchTips/>}/>


      </Routes>
    </BrowserRouter>

  )
}

export default App;