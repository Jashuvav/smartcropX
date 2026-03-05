import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { ENDPOINTS } from "../config/api";
import { useAuth } from "../context/AuthContext";

const PlantDiseaseDetection = () => {
  const { authAxios } = useAuth();
  const [selectedImage, setSelectedImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [detectionResult, setDetectionResult] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isLoaded, setIsLoaded] = useState(false);
  const [isCameraOpen, setIsCameraOpen] = useState(false);
  const [diseases, setDiseases] = useState([
    { name: "Late Blight", count: 12 },
    { name: "Early Blight", count: 8 },
    { name: "Bacterial Spot", count: 5 },
    { name: "Healthy", count: 42 }
  ]);
  const [xaiResult, setXaiResult] = useState(null);
  const [isExplaining, setIsExplaining] = useState(false);
  const [showXai, setShowXai] = useState(false);
  
  const fileInputRef = useRef(null);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    setIsLoaded(true);
    
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedImage(file);
      setPreviewUrl(URL.createObjectURL(file));
      setDetectionResult("");
    }
  };

  const openCamera = async () => {
    try {
      if (!videoRef.current) {
        console.error("Video element is not available");
        alert("Camera initialization failed. Please try again.");
        return;
      }

      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: "environment", width: { ideal: 1280 }, height: { ideal: 720 } }
      });

      streamRef.current = stream;
      videoRef.current.srcObject = stream;
      videoRef.current.onloadedmetadata = () => {
        videoRef.current.play()
          .then(() => setIsCameraOpen(true))
          .catch(err => {
            console.error("Error playing camera feed:", err);
            closeCamera();
          });
      };
    } catch (error) {
      console.error("Error accessing camera:", error);
      alert("Could not access camera. Please allow camera permissions and try again.");
      closeCamera();
    }
  };

  const captureImage = () => {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    
    if (!video || !canvas) {
      console.error("Video or canvas element is not available");
      return;
    }
    
    const context = canvas.getContext('2d');
    
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    canvas.toBlob((blob) => {
      const file = new File([blob], "camera-capture.jpg", { type: "image/jpeg" });
      setSelectedImage(file);
      setPreviewUrl(URL.createObjectURL(blob));
      
      closeCamera();
    }, 'image/jpeg', 0.95);
  };

  const closeCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
    setIsCameraOpen(false);
  };

  const analyzeImage = async () => {
    if (!selectedImage) return;

    setIsAnalyzing(true);
    setDetectionResult("");

    const formData = new FormData();
    formData.append("file", selectedImage);

    try {
      const api = authAxios();
      const response = await api.post(ENDPOINTS.PREDICT_DISEASE, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setDetectionResult(response.data);
    } catch (error) {
      const msg = error.response?.status === 401
        ? "Please log in to use disease detection."
        : error.response?.data?.detail || "Error analyzing image. Please try again.";
      setDetectionResult({ error: msg });
    } finally {
      setIsAnalyzing(false);
    }
  };

  const explainPrediction = async () => {
    if (!selectedImage) return;
    setIsExplaining(true);
    setXaiResult(null);
    const formData = new FormData();
    formData.append("file", selectedImage);
    try {
      const api = authAxios();
      const response = await api.post(ENDPOINTS.EXPLAIN_DISEASE, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setXaiResult(response.data);
      setShowXai(true);
    } catch (error) {
      setXaiResult({ status: "error", explanation: "Could not generate explanation. Try again." });
      setShowXai(true);
    } finally {
      setIsExplaining(false);
    }
  };

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
        <header className="text-center mb-8 pt-6">
          <div 
            className={`transition-all duration-1000 transform ${isLoaded ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-10'}`}
          >
            <button 
              onClick={() => navigate('/')}
              className="absolute left-4 top-4 text-white hover:text-smart-yellow transition-colors"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
              </svg>
            </button>
            
            <p className="text-gray-200 uppercase tracking-wider text-sm mb-2 relative inline-block">
              SMART AGRICULTURAL TOOLS
              <span className="absolute bottom-0 left-0 w-full h-0.5 bg-smart-yellow transform scale-x-0 group-hover:scale-x-100 transition-transform duration-500 origin-left"></span>
            </p>
            <br></br>
            <h1 className="text-white text-4xl md:text-5xl font-bold relative inline-block">
              Plant Disease Detection
              <div className="absolute -bottom-2 left-0 w-full h-1 bg-smart-yellow transform scale-x-0 origin-left transition-transform duration-700" 
                style={{ transform: isLoaded ? 'scaleX(1)' : 'scaleX(0)' }}
              ></div>
            </h1>
          </div>
        </header>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Left section: Upload and camera controls */}
          <div 
            className={`bg-gray-800 bg-opacity-25 backdrop-blur-sm rounded-lg p-6 flex flex-col items-center transition-all duration-500 shadow-lg transform ${isLoaded ? 'translateY(0) opacity-100' : 'translateY(50px) opacity-0'}`}
            style={{ transitionDelay: '200ms' }}
          >
            <div className="relative w-full aspect-square mb-6 bg-black bg-opacity-30 rounded-lg overflow-hidden flex items-center justify-center">
              {isCameraOpen ? (
                <>
                  <video 
                    ref={videoRef}
                    autoPlay
                    muted
                    playsInline
                    className="h-full w-full object-cover"
                  />
                  <canvas ref={canvasRef} className="hidden" />
                </>
              ) : previewUrl ? (
                <img src={previewUrl} alt="Selected plant" className="w-full h-full object-cover" />
              ) : (
                <div className="text-center p-6">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-20 w-20 mx-auto text-smart-yellow opacity-50 mb-4" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clipRule="evenodd" />
                  </svg>
                  <p className="text-gray-300">Upload or capture an image to begin analysis</p>
                </div>
              )}
              
              {isAnalyzing && (
                <div className="absolute inset-0 bg-black bg-opacity-70 flex items-center justify-center">
                  <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-smart-yellow"></div>
                  <p className="absolute text-white mt-24">Analyzing...</p>
                </div>
              )}
            </div>
            
            <div className="grid grid-cols-3 gap-4 w-full">
              <input type="file" accept="image/*" className="hidden" onChange={handleFileChange} ref={fileInputRef} />
              
              <button
                onClick={() => fileInputRef.current.click()}
                className="col-span-1 bg-black bg-opacity-30 hover:bg-opacity-50 text-white py-3 px-4 rounded-lg flex items-center justify-center transition-all duration-300 group"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-smart-yellow group-hover:scale-110 transition-transform duration-300" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM6.293 6.707a1 1 0 010-1.414l3-3a1 1 0 011.414 0l3 3a1 1 0 01-1.414 1.414L11 5.414V13a1 1 0 11-2 0V5.414L7.707 6.707a1 1 0 01-1.414 0z" clipRule="evenodd" />
                </svg>
                Upload
              </button>
              
              {isCameraOpen ? (
                <>
                  <button
                    onClick={captureImage}
                    className="col-span-1 bg-smart-yellow text-smart-green py-3 px-4 rounded-lg flex items-center justify-center transition-all duration-300 hover:bg-opacity-90"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M4 5a2 2 0 00-2 2v8a2 2 0 002 2h12a2 2 0 002-2V7a2 2 0 00-2-2h-1.586a1 1 0 01-.707-.293l-1.121-1.121A2 2 0 0011.172 3H8.828a2 2 0 00-1.414.586L6.293 4.707A1 1 0 015.586 5H4zm6 9a3 3 0 100-6 3 3 0 000 6z" clipRule="evenodd" />
                    </svg>
                    Capture
                  </button>
                  
                  <button
                    onClick={closeCamera}
                    className="col-span-1 bg-red-500 text-white py-3 px-4 rounded-lg flex items-center justify-center transition-all duration-300 hover:bg-opacity-90"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                    </svg>
                    Cancel
                  </button>
                </>
              ) : (
                <>
                  <button
                    onClick={openCamera}
                    className="col-span-1 bg-black bg-opacity-30 hover:bg-opacity-50 text-white py-3 px-4 rounded-lg flex items-center justify-center transition-all duration-300 group"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-smart-yellow group-hover:scale-110 transition-transform duration-300" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M4 5a2 2 0 00-2 2v8a2 2 0 002 2h12a2 2 0 002-2V7a2 2 0 00-2-2h-1.586a1 1 0 01-.707-.293l-1.121-1.121A2 2 0 0011.172 3H8.828a2 2 0 00-1.414.586L6.293 4.707A1 1 0 015.586 5H4zm6 9a3 3 0 100-6 3 3 0 000 6z" clipRule="evenodd" />
                    </svg>
                    Camera
                  </button>
                  
                  <button
                    onClick={analyzeImage}
                    disabled={!selectedImage || isAnalyzing}
                    className={`col-span-1 py-3 px-4 rounded-lg flex items-center justify-center transition-all duration-300 ${
                      !selectedImage || isAnalyzing
                        ? "bg-gray-500 text-gray-300 cursor-not-allowed"
                        : "bg-smart-yellow text-smart-green hover:bg-opacity-90"
                    }`}
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M6.625 2.655A9 9 0 0119 11a1 1 0 11-2 0 7 7 0 00-9.625-6.492 1 1 0 11-.75-1.853zM4.662 4.959A1 1 0 014.75 6.37 6.97 6.97 0 003 11a1 1 0 11-2 0 8.97 8.97 0 012.25-5.953 1 1 0 011.412-.088z" clipRule="evenodd" />
                      <path fillRule="evenodd" d="M5 11a5 5 0 1110 0 1 1 0 11-2 0 3 3 0 10-6 0c0 1.677-.345 3.276-.968 4.729a1 1 0 11-1.838-.789A9.964 9.964 0 005 11z" clipRule="evenodd" />
                    </svg>
                    Analyze
                  </button>
                </>
              )}
            </div>
            
            {detectionResult && !isCameraOpen && (
              <div className="mt-6 w-full bg-black bg-opacity-30 backdrop-blur-sm rounded-lg p-4 text-white animate-fadeIn">
                <h3 className="text-lg font-bold text-smart-yellow border-b border-gray-700 pb-2 mb-3">Analysis Results</h3>
                
                {detectionResult.error ? (
                  <div className="p-3 bg-red-900 bg-opacity-30 rounded-lg text-red-300">
                    <p className="flex items-center">
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                      </svg>
                      {detectionResult.error}
                    </p>
                    <p className="text-sm mt-2">Please try again with a clearer image.</p>
                  </div>
                ) : (
                  <div>
                    <div className="grid grid-cols-2 gap-4 mb-4">
                      <div className="bg-black bg-opacity-30 p-3 rounded-lg">
                        <p className="text-gray-400 text-sm">Disease</p>
                        <p className="text-xl font-bold">{detectionResult.class}</p>
                      </div>
                      
                      <div className="bg-black bg-opacity-30 p-3 rounded-lg">
                        <p className="text-gray-400 text-sm">Confidence</p>
                        <p className="text-xl font-bold">{(detectionResult.confidence * 100).toFixed(1)}%</p>
                      </div>
                    </div>
                    
                    <div className="bg-black bg-opacity-30 p-3 rounded-lg flex items-center">
                      <div className={`w-3 h-3 rounded-full mr-2 ${detectionResult.status === "HEALTHY" ? "bg-green-500" : "bg-red-500"}`}></div>
                      <p>Status: <span className={detectionResult.status === "HEALTHY" ? "text-green-400" : "text-red-400"}>{detectionResult.status}</span></p>
                    </div>
                    
                    {detectionResult.treatment && (
                      <div className="mt-4 bg-black bg-opacity-30 p-3 rounded-lg">
                        <p className="text-gray-400 text-sm mb-1">Recommended Treatment:</p>
                        <p>{detectionResult.treatment}</p>
                      </div>
                    )}

                    {/* XAI: Explain button */}
                    <button
                      onClick={explainPrediction}
                      disabled={isExplaining}
                      className="mt-4 w-full py-2 px-4 rounded-lg bg-purple-600 hover:bg-purple-500 text-white font-medium transition-all duration-300 flex items-center justify-center"
                    >
                      {isExplaining ? (
                        <><svg className="animate-spin h-5 w-5 mr-2" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"/><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>Generating Explanation...</>
                      ) : (
                        <><svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor"><path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-3a1 1 0 00-.867.5 1 1 0 11-1.731-1A3 3 0 0113 8a3.001 3.001 0 01-2 2.83V11a1 1 0 11-2 0v-1a1 1 0 011-1 1 1 0 100-2zm0 8a1 1 0 100-2 1 1 0 000 2z" clipRule="evenodd"/></svg>Why this prediction? (XAI)</>
                      )}
                    </button>

                    {/* XAI: Grad-CAM Results */}
                    {showXai && xaiResult && (
                      <div className="mt-4 bg-black bg-opacity-40 rounded-lg p-4 animate-fadeIn">
                        <div className="flex items-center justify-between mb-3">
                          <h4 className="text-lg font-bold text-purple-300 flex items-center">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor"><path d="M10 12a2 2 0 100-4 2 2 0 000 4z"/><path fillRule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clipRule="evenodd"/></svg>
                            Explainable AI — Grad-CAM
                          </h4>
                          <button onClick={() => setShowXai(false)} className="text-gray-400 hover:text-white text-sm">✕ Close</button>
                        </div>

                        {xaiResult.status === "error" ? (
                          <p className="text-red-300 text-sm">{xaiResult.explanation}</p>
                        ) : (
                          <>
                            <p className="text-gray-300 text-sm mb-3">{xaiResult.explanation}</p>
                            <span className="inline-block mb-2 text-xs px-2 py-1 rounded bg-purple-900 text-purple-200">
                              Method: {xaiResult.method}
                            </span>

                            <div className="grid grid-cols-2 gap-3 mt-2">
                              {xaiResult.heatmap && (
                                <div>
                                  <p className="text-gray-400 text-xs mb-1">Activation Heatmap</p>
                                  <img src={xaiResult.heatmap} alt="Grad-CAM heatmap" className="w-full rounded-lg border border-purple-700"/>
                                </div>
                              )}
                              {xaiResult.overlay && (
                                <div>
                                  <p className="text-gray-400 text-xs mb-1">Overlay on Original</p>
                                  <img src={xaiResult.overlay} alt="Grad-CAM overlay" className="w-full rounded-lg border border-purple-700"/>
                                </div>
                              )}
                            </div>

                            {xaiResult.regions && xaiResult.regions.length > 0 && (
                              <div className="mt-3">
                                <p className="text-gray-400 text-xs mb-1">Top Activation Regions</p>
                                <div className="space-y-1">
                                  {xaiResult.regions.map((r, i) => (
                                    <div key={i} className="flex items-center text-sm">
                                      <span className="text-purple-300 mr-2">#{i+1}</span>
                                      <div className="flex-1 bg-gray-700 rounded-full h-2">
                                        <div className="bg-purple-500 rounded-full h-2" style={{width: `${r.intensity * 100}%`}}/>
                                      </div>
                                      <span className="text-gray-400 ml-2 text-xs">{(r.intensity * 100).toFixed(0)}%</span>
                                    </div>
                                  ))}
                                </div>
                              </div>
                            )}
                          </>
                        )}
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
          
          <div className="flex flex-col gap-6">
            <div 
              className={`bg-gray-800 bg-opacity-25 backdrop-blur-sm rounded-lg p-6 transition-all duration-500 shadow-lg transform ${isLoaded ? 'translateY(0) opacity-100' : 'translateY(50px) opacity-0'}`}
              style={{ transitionDelay: '300ms' }}
            >
              <h3 className="text-xl font-bold text-white mb-4 flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 mr-2 text-smart-yellow" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                </svg>
                How It Works
              </h3>
              
              <div className="space-y-4 text-gray-200 text-sm">
                <p>Our AI-powered plant disease detection system uses computer vision to identify diseases in crops. The system is trained on thousands of images of healthy and diseased plants.</p>
                
                <div className="bg-black bg-opacity-30 p-3 rounded-lg">
                  <p className="font-medium mb-2">Simple 3-step process:</p>
                  <ol className="list-decimal pl-5 space-y-1">
                    <li>Upload or capture a clear image of the affected plant</li>
                    <li>Our AI analyzes the image for disease patterns</li>
                    <li>Receive instant identification and treatment advice</li>
                  </ol>
                </div>
                
                <p>For best results, take close-up images of affected leaves or stems in good lighting conditions.</p>
              </div>
            </div>
            
            <div 
              className={`bg-gray-800 bg-opacity-25 backdrop-blur-sm rounded-lg p-6 transition-all duration-500 shadow-lg transform ${isLoaded ? 'translateY(0) opacity-100' : 'translateY(50px) opacity-0'}`}
              style={{ transitionDelay: '400ms' }}
            >
              <h3 className="text-xl font-bold text-white mb-4 flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 mr-2 text-smart-yellow" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M2 10a8 8 0 018-8v8h8a8 8 0 11-16 0z" />
                  <path d="M12 2.252A8.014 8.014 0 0117.748 8H12V2.252z" />
                </svg>
                Recent Farm Statistics
              </h3>
              
              <div className="space-y-3">
                <p className="text-gray-300 text-sm mb-2">Common diseases detected on your farm:</p>
                
                {diseases.map((disease, index) => (
                  <div key={index} className="bg-black bg-opacity-30 rounded-lg p-3">
                    <div className="flex justify-between items-center mb-1">
                      <span className="text-white">{disease.name}</span>
                      <span className="text-sm text-gray-400">{disease.count} cases</span>
                    </div>
                    <div className="w-full bg-gray-700 rounded-full h-2">
                      <div 
                        className={`h-2 rounded-full ${disease.name === "Healthy" ? "bg-green-500" : "bg-red-500"}`} 
                        style={{ width: `${(disease.count / Math.max(...diseases.map(d => d.count))) * 100}%` }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div 
        className={`fixed bottom-6 right-6 z-20 transition-all duration-700 transform ${isLoaded ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}
        style={{ transitionDelay: '1000ms' }}
      >
        <button 
          onClick={() => navigate('/')}
          className="w-14 h-14 rounded-full bg-smart-yellow text-smart-green flex items-center justify-center shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-110"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clipRule="evenodd" />
          </svg>
        </button>
      </div>

      <style jsx>{`
        @keyframes float {
          0% { transform: translateY(0) rotate(0deg); }
          50% { transform: translateY(-20px) rotate(180deg); }
          100% { transform: translateY(0) rotate(360deg); }
        }
        
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        
        .animate-fadeIn {
          animation: fadeIn 0.5s ease-out forwards;
        }
      `}</style>
    </div>
  );
};

export default PlantDiseaseDetection;