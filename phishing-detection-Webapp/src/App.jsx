import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import Header from "./components/Header";
import Hero from "./components/Hero"
import URLScan from "./components/URLScan";
import Footer from "./components/Footer";
import './App.css'

function App() {
  return (
    <div className="App">
      <Header classsName="header"/>
      <Hero className="hero"/>
      <URLScan className="url-scan"/>
      <Footer className="footer"/>
    </div>
  )
}

export default App;
