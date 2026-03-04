// API Configuration
const API_CONFIG = {
  // Production API URL (your deployed backend)
  PRODUCTION_URL: "https://smartcropx.onrender.com",
  
  // Development API URL (for local development)
  DEVELOPMENT_URL: "http://localhost:8001",
  
  // Get the current API URL based on environment
  getApiUrl: () => {
    // Check if we're in production
    if (window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
      return API_CONFIG.PRODUCTION_URL;
    }
    
    // Use development URL for local development
    return API_CONFIG.DEVELOPMENT_URL;
  }
};

// Export the API URL
export const API_URL = API_CONFIG.getApiUrl();

// Export individual endpoints
export const ENDPOINTS = {
  PREDICT_DISEASE: `${API_URL}/predict`,
  PREDICT_SOIL: `${API_URL}/predict-soil`,
  MARKET_PREDICTIONS: `${API_URL}/market-predictions`,
  WEATHER_FORECAST: `${API_URL}/weather-forecast`,
  WEATHER_CURRENT: `${API_URL}/weather-current`,
  WEATHER_ALERTS: `${API_URL}/weather-alerts`,
  HEALTH_CHECK: `${API_URL}/health`,
  DETAILED_HEALTH: `${API_URL}/healthz`,
  // XAI – Explainable AI endpoints
  EXPLAIN_DISEASE: `${API_URL}/api/disease/explain`,
  EXPLAIN_SOIL: `${API_URL}/api/soil/explain`,
  EXPLAIN_PRICE: `${API_URL}/api/price/explain`,     // GET /{crop}
  EXPLAIN_PRICE_ALL: `${API_URL}/api/price/explain`,  // GET (all crops)
  // Chatbot
  CHAT: `${API_URL}/api/chat`,
  CHAT_HEALTH: `${API_URL}/api/chat/health`,
  API_HEALTH: `${API_URL}/api/health`,
  // Recommendation
  RECOMMEND_CROP: `${API_URL}/api/recommend/crop`,
  RECOMMEND_SOIL: `${API_URL}/api/recommend/soil`,
  RECOMMEND_HEALTH: `${API_URL}/api/recommend/health`,
  // Pesticide
  PESTICIDE_RECOMMEND: `${API_URL}/api/pesticide/recommend`,
  PESTICIDE_DISEASES: `${API_URL}/api/pesticide/diseases`,
  PESTICIDE_CROPS: `${API_URL}/api/pesticide/crops`,
  PESTICIDE_HEALTH: `${API_URL}/api/pesticide/health`,
};

export default API_CONFIG;
