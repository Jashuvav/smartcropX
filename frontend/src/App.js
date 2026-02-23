import React, { useEffect, useState } from 'react';
import "./App.css";
import Header from './pages/Header';
import HeroSection from './pages/HeroSection';
import Agriinfo from './pages/OrganicFarmUI';
import Dashboard from './pages/AgriDashboard';
import News from './pages/AgriNewsSection';
import ContactUs from './pages/ContactUs';
import PlantDiseaseDetection from './pages/PlantDiseaseDetection';
import MarketPrediction from './pages/MarketPrediction';
import WeatherForecast from './pages/WeatherForecast';
import StorageForm from "./components/StorageForm";  
import Marketplace from "./components/Marketplace"; 
import SoilPredictor from './pages/SoilPredictor';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ApiTestPage from './pages/ApiTestPage';
import CommunityFeed from './pages/CommunityFeed';
import CreatePost from './pages/CreatePost';
import PostDetail from './pages/PostDetail';
import { AuthProvider } from './context/AuthContext';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

function App() {
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    setLoaded(true);
    
    const checkVisibility = () => {
      const sections = document.querySelectorAll('.scroll-reveal');
      const windowHeight = window.innerHeight;
      
      sections.forEach(section => {
        const boundingRect = section.getBoundingClientRect();
        if (boundingRect.top < windowHeight * 0.85) {
          section.classList.add('visible');
        }
      });
    };
    
    setTimeout(checkVisibility, 100);
    
    let scrollTimeout;
    const handleScroll = () => {
      if (!scrollTimeout) {
        scrollTimeout = setTimeout(() => {
          checkVisibility();
          scrollTimeout = null;
        }, 10);
      }
    };
    
    window.addEventListener('scroll', handleScroll);
    
    return () => {
      window.removeEventListener('scroll', handleScroll);
      clearTimeout(scrollTimeout);
    };
  }, []);

  return (
    <AuthProvider>
    <Router>
      <div className={`App ${loaded ? 'app-loaded' : ''}`}>
        <div className="header-container">
          <Header />
        </div>
        
        <Routes>
          <Route path="/disease-detection" element={<PlantDiseaseDetection />} />
          <Route path="/market-prediction" element={<MarketPrediction />} />
          <Route path="/weather-prediction" element={<WeatherForecast />} />
          <Route path="/StorageForm" element={<StorageForm />} />
          <Route path="/Marketplace" element={<Marketplace />} />
          <Route path="/LoginPage" element={<LoginPage />} />
          <Route path="/RegisterPage" element={<RegisterPage />} />
          <Route path="/SoilPredictor" element={<SoilPredictor />} />
          <Route path="/api-test" element={<ApiTestPage />} />
          <Route path="/community" element={<CommunityFeed />} />
          <Route path="/community/new" element={<CreatePost />} />
          <Route path="/community/post/:id" element={<PostDetail />} />
          <Route path="/" element={
            <div className="content-container">
              <div className="scroll-reveal">
                <HeroSection />
              </div>
              <div className="scroll-reveal">
                <Agriinfo />
              </div>
              <div className="scroll-reveal">
                <Dashboard />
              </div>
              <div className="scroll-reveal">
                <News />
              </div>
              <div className="scroll-reveal">
                <ContactUs />
              </div>
            </div>
          } />
        </Routes>
      </div>
    </Router>
    </AuthProvider>
  );
}

export default App;