const DEFAULT_LOCAL_API_URL = "http://localhost:8013";

const normalizeUrl = (url) => url.replace(/\/$/, "");

// API Configuration
const API_CONFIG = {
  DEFAULT_LOCAL_API_URL,

  getApiUrl: () => {
    const configuredUrl = process.env.REACT_APP_API_URL?.trim();
    if (configuredUrl) {
      return normalizeUrl(configuredUrl);
    }

    const isLocalHost = ["localhost", "127.0.0.1"].includes(window.location.hostname);
    if (isLocalHost) {
      return DEFAULT_LOCAL_API_URL;
    }

    return normalizeUrl(window.location.origin);
  }
};

// Export the API URL
export const API_URL = API_CONFIG.getApiUrl();

// Export individual endpoints
export const ENDPOINTS = {
  PREDICT_DISEASE: `${API_URL}/predict`,
  PREDICT_SOIL: `${API_URL}/predict-soil`,
  WEATHER_FORECAST: `${API_URL}/weather-forecast`,
  WEATHER_CURRENT: `${API_URL}/weather-current`,
  WEATHER_ALERTS: `${API_URL}/weather-alerts`,
  HEALTH_CHECK: `${API_URL}/health`,
  DETAILED_HEALTH: `${API_URL}/healthz`,
  // XAI – Explainable AI endpoints
  EXPLAIN_DISEASE: `${API_URL}/api/disease/explain`,
  EXPLAIN_SOIL: `${API_URL}/api/soil/explain`,
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
