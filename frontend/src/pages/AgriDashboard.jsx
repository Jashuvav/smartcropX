import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const AgriDashboard = () => {
  const [isLoaded, setIsLoaded] = useState(false);
  const [weatherData, setWeatherData] = useState({ temp: 28, humidity: 65 });
  const navigate = useNavigate();
  const { user } = useAuth();
  
  useEffect(() => {
    setIsLoaded(true);
    const interval = setInterval(() => {
      setWeatherData({
        temp: Math.floor(25 + Math.random() * 5),
        humidity: Math.floor(60 + Math.random() * 10)
      });
    }, 5000);
    
    return () => clearInterval(interval);
  }, []);
  
  const handleCardClick = (cardId) => {
    switch(cardId) {
      case 1:
        navigate('/crop-recommendation');
        break;
      case 2:
        navigate('/pesticide-recommendation');
        break;
      case 3: 
        navigate('/disease-detection');
        break;
      case 4: 
        navigate('/weather-prediction');
        break;
      case 5: 
        navigate('/SoilPredictor');
        break;
      case 6: 
        navigate('/community');
        break;
      default:
        break;
    }
  };
  
  const allCards = [
    {
      id: 1,
      title: "Crop Recommendation",
      description: "AI-powered crop suggestions based on your soil, weather & location",
      roles: ['FARMER', 'AGRONOMIST', 'ADMIN'],
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-12 h-12 text-smart-yellow group-hover:text-smart-green transition-colors duration-300">
          <path d="M12 22c4-4 8-7.5 8-12a8 8 0 10-16 0c0 4.5 4 8 8 12z" />
          <path d="M12 8v4" />
          <path d="M12 16h.01" />
        </svg>
      ),
    },
    {
      id: 2,
      title: "Pesticide Recommendation",
      description: "Get expert pesticide advice based on disease and crop type",
      roles: ['FARMER', 'ADMIN'],
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-12 h-12 text-smart-yellow group-hover:text-smart-green transition-colors duration-300">
          <path d="M9 3h6v2H9zM12 5v6M7 11h10l1 11H6l1-11z" />
        </svg>
      ),
    },
    {
      id: 3,
      title: "Plant Disease Detection",
      description: "Identify plant diseases using image processing",
      roles: ['FARMER', 'AGRONOMIST', 'ADMIN'],
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-12 h-12 text-smart-yellow group-hover:text-smart-green transition-colors duration-300">
          <path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          <path d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
        </svg>
      ),
    },
    {
      id: 4,
      title: "Weather Prediction",
      description: "Real-time weather forecasts for your farm location",
      roles: ['FARMER', 'AGRONOMIST', 'ADMIN'],
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-12 h-12 text-smart-yellow group-hover:text-smart-green transition-colors duration-300">
          <path d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z" />
        </svg>
      ),
    },
    {
      id: 5,
      title: "Soil Detection",
      description: "Know what crops to plant based on your soil type",
      roles: ['FARMER', 'ADMIN'],
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-12 h-12 text-smart-yellow group-hover:text-smart-green transition-colors duration-300">
          <path d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
        </svg>
      ),
    },
    {
      id: 6,
      title: "Community",
      description: "Connect with farmers, share knowledge & ask questions",
      roles: ['FARMER', 'AGRONOMIST', 'ADMIN'],
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-12 h-12 text-smart-yellow group-hover:text-smart-green transition-colors duration-300">
          <path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2" />
          <circle cx="9" cy="7" r="4" />
          <path d="M23 21v-2a4 4 0 00-3-3.87" />
          <path d="M16 3.13a4 4 0 010 7.75" />
        </svg>
      ),
    }
  ];

  // Role-based card filtering
  const userRole = (user?.role || 'FARMER').toUpperCase();
  const dashboardCards = allCards.filter(card => card.roles.includes(userRole));

  return (
    <div className="w-full min-h-screen bg-gradient-to-b from-smart-green to-green-900 p-6 overflow-hidden">
      <div className="fixed inset-0 z-0 opacity-10">
        {[...Array(20)].map((_, i) => (
          <div 
            key={i}
            className="absolute rounded-full bg-white"
            style={{
              width: `${Math.random() * 8 + 2}px`,
              height: `${Math.random() * 8 + 2}px`,
              top: `${Math.random() * 100}%`,
              left: `${Math.random() * 100}%`,
              animation: `float ${Math.random() * 10 + 10}s linear infinite`,
              animationDelay: `${Math.random() * 5}s`
            }}
          />
        ))}
      </div>
      
      <div className="max-w-6xl mx-auto relative z-10">
        <header className="text-center mb-12 pt-6">
          <div 
            className={`transition-all duration-1000 transform ${isLoaded ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-10'}`}
          >
            <p className="text-gray-200 uppercase tracking-wider text-sm mb-2 relative inline-block">
              SMART AGRICULTURAL TOOLS
              <span className="absolute bottom-0 left-0 w-full h-0.5 bg-smart-yellow transform scale-x-0 group-hover:scale-x-100 transition-transform duration-500 origin-left"></span>
            </p>
            <br></br>
            <h1 className="text-white text-4xl md:text-5xl font-bold relative inline-block">
              Smart Farming Dashboard
              <div className="absolute -bottom-2 left-0 w-full h-1 bg-smart-yellow transform scale-x-0 origin-left transition-transform duration-700" 
                style={{ transform: isLoaded ? 'scaleX(1)' : 'scaleX(0)' }}
              ></div>
            </h1>
          </div>
          
          <div 
            className={`mt-6 inline-flex items-center bg-black bg-opacity-25 rounded-full px-4 py-2 text-white transition-all duration-700 ${isLoaded ? 'opacity-100 scale-100' : 'opacity-0 scale-95'}`}
            style={{ transitionDelay: '400ms' }}
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-smart-yellow" viewBox="0 0 20 20" fill="currentColor">
              <path d="M5.5 16a3.5 3.5 0 01-.369-6.98 4 4 0 117.753-1.977A4.5 4.5 0 1113.5 16h-8z" />
            </svg>
            <span>{weatherData.temp}°C</span>
            <span className="mx-2">|</span>
            <span>Humidity: {weatherData.humidity}%</span>
          </div>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 justify-items-center">
          {dashboardCards.map((card, index) => (
            <div
              key={card.id}
              className="cursor-pointer"
              onClick={() => handleCardClick(card.id)}
              style={{
                transform: isLoaded ? 'translateY(0)' : 'translateY(50px)',
                opacity: isLoaded ? 1 : 0,
                transition: 'transform 0.5s ease-out, opacity 0.5s ease-out',
                transitionDelay: `${index * 100}ms`,
              }}
            >
              <div className="group flex flex-col items-center justify-center p-6 bg-gray-900/80 border border-gray-700 rounded-xl transition-all duration-200 hover:shadow-lg hover:scale-[1.01]">
                <div className="w-16 h-16 mb-4 flex items-center justify-center">
                  {card.icon}
                </div>
                <h3 className="font-bold text-lg text-center text-smart-yellow mb-2">
                  {card.title}
                </h3>
                <p className="text-gray-300 text-sm text-center px-2">
                  {card.description}
                </p>
                <div className="mt-4 w-3/4">
                  <span className="block w-full py-1.5 px-3 bg-smart-green text-white text-sm rounded text-center hover:bg-opacity-90 transition-all duration-300">
                    Open →
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
        
        <div 
          className="mt-12 bg-black bg-opacity-30 backdrop-blur-sm rounded-xl p-4 grid grid-cols-1 md:grid-cols-4 gap-4 text-white"
          style={{ 
            transform: isLoaded ? 'translateY(0)' : 'translateY(30px)',
            opacity: isLoaded ? 1 : 0,
            transition: 'transform 0.7s ease-out, opacity 0.7s ease-out',
            transitionDelay: '700ms'
          }}
        >
          <div className="flex items-center p-2 border-b md:border-b-0 md:border-r border-gray-600">
            <div className="w-10 h-10 rounded-full bg-green-500 bg-opacity-30 flex items-center justify-center mr-3">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                <path d="M2 10a8 8 0 018-8v8h8a8 8 0 11-16 0z" />
                <path d="M12 2.252A8.014 8.014 0 0117.748 8H12V2.252z" />
              </svg>
            </div>
            <div>
              <p className="text-gray-400 text-xs">Total Crops</p>
              <p className="text-xl font-bold">12,450</p>
            </div>
          </div>
          
          <div className="flex items-center p-2 border-b md:border-b-0 md:border-r border-gray-600">
            <div className="w-10 h-10 rounded-full bg-blue-500 bg-opacity-30 flex items-center justify-center mr-3">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-blue-400" viewBox="0 0 20 20" fill="currentColor">
                <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z" />
              </svg>
            </div>
            <div>
              <p className="text-gray-400 text-xs">Farm Workers</p>
              <p className="text-xl font-bold">24</p>
            </div>
          </div>
          
          <div className="flex items-center p-2 border-b md:border-b-0 md:border-r border-gray-600">
            <div className="w-10 h-10 rounded-full bg-yellow-500 bg-opacity-30 flex items-center justify-center mr-3">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M5 2a1 1 0 011 1v1h1a1 1 0 010 2H6v1a1 1 0 01-2 0V6H3a1 1 0 010-2h1V3a1 1 0 011-1zm0 10a1 1 0 011 1v1h1a1 1 0 110 2H6v1a1 1 0 11-2 0v-1H3a1 1 0 110-2h1v-1a1 1 0 011-1zM12 2a1 1 0 01.967.744L14.146 7.2 17.5 9.134a1 1 0 010 1.732l-3.354 1.935-1.18 4.455a1 1 0 01-1.933 0L9.854 12.8 6.5 10.866a1 1 0 010-1.732l3.354-1.935 1.18-4.455A1 1 0 0112 2z" clipRule="evenodd" />
              </svg>
            </div>
            <div>
              <p className="text-gray-400 text-xs">Harvests</p>
              <p className="text-xl font-bold">6.2 tons</p>
            </div>
          </div>
          
          <div className="flex items-center p-2">
            <div className="w-10 h-10 rounded-full bg-purple-500 bg-opacity-30 flex items-center justify-center mr-3">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-purple-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clipRule="evenodd" />
              </svg>
            </div>
            <div>
              <p className="text-gray-400 text-xs">Growing Cycles</p>
              <p className="text-xl font-bold">3 active</p>
            </div>
          </div>
        </div>
      </div>
      
      <div 
        className={`fixed bottom-6 right-6 z-20 transition-all duration-700 transform ${isLoaded ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}
        style={{ transitionDelay: '1000ms' }}
      >
        <button className="w-14 h-14 rounded-full bg-smart-yellow text-smart-green flex items-center justify-center shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-110">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
          </svg>
        </button>
      </div>

      <style jsx>{`
        @keyframes float {
          0% { transform: translateY(0) rotate(0deg); }
          50% { transform: translateY(-20px) rotate(180deg); }
          100% { transform: translateY(0) rotate(360deg); }
        }
      `}</style>
    </div>
  );
};

export default AgriDashboard;