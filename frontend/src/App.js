import React, { useEffect, useState } from 'react';
import "./App.css";
import Header from './pages/Header';
import HeroSection from './pages/HeroSection';
import Agriinfo from './pages/OrganicFarmUI';
import Dashboard from './pages/AgriDashboard';
import News from './pages/AgriNewsSection';
import ContactUs from './pages/ContactUs';
import PlantDiseaseDetection from './pages/PlantDiseaseDetection';
import WeatherForecast from './pages/WeatherForecast';
import SoilPredictor from './pages/SoilPredictor';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import CommunityFeed from './pages/CommunityFeed';
import CreatePost from './pages/CreatePost';
import PostDetail from './pages/PostDetail';
import { AuthProvider } from './context/AuthContext';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ProtectedRoute from './components/ProtectedRoute';
import CropRecommendation from './pages/CropRecommendation';
import SoilRecommendation from './pages/SoilRecommendation';
import PesticideRecommendation from './pages/PesticideRecommendation';
import AllNews from './pages/AllNews';

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
          <Route path="/disease-detection" element={<ProtectedRoute roles={['FARMER','AGRONOMIST','ADMIN']}><PlantDiseaseDetection /></ProtectedRoute>} />
          <Route path="/weather-prediction" element={<ProtectedRoute roles={['FARMER','AGRONOMIST','ADMIN']}><WeatherForecast /></ProtectedRoute>} />
          <Route path="/LoginPage" element={<LoginPage />} />
          <Route path="/RegisterPage" element={<RegisterPage />} />
          <Route path="/SoilPredictor" element={<ProtectedRoute roles={['FARMER','ADMIN']}><SoilPredictor /></ProtectedRoute>} />
          <Route path="/community" element={<CommunityFeed />} />
          <Route path="/community/new" element={<CreatePost />} />
          <Route path="/community/post/:id" element={<PostDetail />} />
          <Route path="/crop-recommendation" element={<CropRecommendation />} />
          <Route path="/soil-recommendation" element={<SoilRecommendation />} />
          <Route path="/pesticide-recommendation" element={<ProtectedRoute roles={['FARMER','ADMIN']}><PesticideRecommendation /></ProtectedRoute>} />
          <Route path="/news" element={<AllNews />} />
          <Route path="/" element={
            <div className="content-container">
              <div className="scroll-reveal">
                <HeroSection />
              </div>
              <div id="agriinfo" className="scroll-reveal">
                <Agriinfo />
              </div>
              <div id="dashboard" className="scroll-reveal">
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