import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { API_URL } from '../config/api';
import {
  Bug, Leaf, FlaskConical, ShieldCheck, AlertCircle,
  Loader2, Search, Sprout, Info, ChevronDown,
} from 'lucide-react';

const PesticideRecommendation = () => {
  const [disease, setDisease] = useState('');
  const [crop, setCrop] = useState('');
  const [crops, setCrops] = useState([]);
  const [diseases, setDiseases] = useState([]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  // Pre-populate from URL query params (linked from Disease Detection)
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    if (params.get('disease')) setDisease(params.get('disease'));
    if (params.get('crop')) setCrop(params.get('crop'));
  }, []);

  // Fetch available diseases & crops from backend
  useEffect(() => {
    const fetchMeta = async () => {
      try {
        const [dRes, cRes] = await Promise.all([
          axios.get(`${API_URL}/api/pesticide/diseases`).catch(() => ({ data: { diseases: [] } })),
          axios.get(`${API_URL}/api/pesticide/crops`).catch(() => ({ data: { crops: [] } })),
        ]);
        setDiseases(dRes.data.diseases || []);
        setCrops(cRes.data.crops || []);
      } catch { /* ignore */ }
    };
    fetchMeta();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!disease.trim()) {
      setError('Please enter a disease name.');
      return;
    }
    setError('');
    setResult(null);
    setLoading(true);
    try {
      const payload = { disease: disease.trim(), crop: crop.trim() || undefined };
      const res = await axios.post(`${API_URL}/api/pesticide/recommend`, payload, { timeout: 10000 });
      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to get recommendation. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 pt-24 pb-16 px-4">
      <div className="max-w-3xl mx-auto">
        {/* Header */}
        <div className="text-center mb-10">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gradient-to-br from-green-500 to-emerald-600 shadow-lg mb-4">
            <ShieldCheck className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-3xl md:text-4xl font-bold text-gray-800 mb-2">
            Pesticide Recommendation
          </h1>
          <p className="text-gray-500 max-w-xl mx-auto">
            Enter the detected plant disease and crop to get an expert pesticide recommendation
            with dosage and application instructions.
          </p>
        </div>

        {/* Form Card */}
        <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl border border-green-100 p-6 md:p-8 mb-8">
          <form onSubmit={handleSubmit} className="space-y-5">
            {/* Disease input */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-1.5 flex items-center gap-1.5">
                <Bug className="w-4 h-4 text-red-500" /> Disease Name
              </label>
              <div className="relative">
                <input
                  list="disease-options"
                  type="text"
                  value={disease}
                  onChange={(e) => setDisease(e.target.value)}
                  placeholder="e.g. Early Blight, Blast, Rust..."
                  className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-green-400 focus:border-transparent outline-none transition text-gray-800 bg-gray-50"
                  required
                />
                <datalist id="disease-options">
                  {diseases.map((d) => (
                    <option key={d} value={d} />
                  ))}
                </datalist>
              </div>
            </div>

            {/* Crop input */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-1.5 flex items-center gap-1.5">
                <Sprout className="w-4 h-4 text-green-600" /> Crop (optional)
              </label>
              <div className="relative">
                <select
                  value={crop}
                  onChange={(e) => setCrop(e.target.value)}
                  className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-green-400 focus:border-transparent outline-none transition text-gray-800 bg-gray-50 appearance-none"
                >
                  <option value="">— Any crop —</option>
                  {crops.map((c) => (
                    <option key={c} value={c}>{c}</option>
                  ))}
                </select>
                <ChevronDown className="absolute right-3 top-3.5 w-4 h-4 text-gray-400 pointer-events-none" />
              </div>
            </div>

            {/* Submit */}
            <button
              type="submit"
              disabled={loading}
              className="w-full py-3.5 rounded-xl font-semibold text-white bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 transition-all shadow-md hover:shadow-lg disabled:opacity-60 flex items-center justify-center gap-2"
            >
              {loading ? (
                <><Loader2 className="w-5 h-5 animate-spin" /> Analysing…</>
              ) : (
                <><Search className="w-5 h-5" /> Get Recommendation</>
              )}
            </button>
          </form>

          {error && (
            <div className="mt-4 flex items-start gap-2 text-red-600 bg-red-50 rounded-lg p-3 text-sm">
              <AlertCircle className="w-5 h-5 mt-0.5 shrink-0" />
              <span>{error}</span>
            </div>
          )}
        </div>

        {/* Result Card */}
        {result && (
          <div className={`rounded-2xl shadow-xl border p-6 md:p-8 transition-all ${
            result.matched
              ? 'bg-white/90 border-green-200'
              : 'bg-yellow-50/90 border-yellow-200'
          }`}>
            <div className="flex items-center gap-3 mb-5">
              <div className={`w-12 h-12 rounded-full flex items-center justify-center ${
                result.matched ? 'bg-green-100' : 'bg-yellow-100'
              }`}>
                <FlaskConical className={`w-6 h-6 ${result.matched ? 'text-green-600' : 'text-yellow-600'}`} />
              </div>
              <div>
                <h2 className="text-xl font-bold text-gray-800">{result.pesticide}</h2>
                <p className="text-sm text-gray-500">
                  For <span className="font-medium text-gray-700">{result.disease}</span>
                  {result.crop !== 'General' && (
                    <> on <span className="font-medium text-green-700">{result.crop}</span></>
                  )}
                </p>
              </div>
            </div>

            <div className="grid gap-4 md:grid-cols-2">
              {/* Dosage */}
              <div className="bg-gradient-to-br from-blue-50 to-blue-100/60 rounded-xl p-4">
                <div className="flex items-center gap-2 mb-2">
                  <Leaf className="w-5 h-5 text-blue-600" />
                  <span className="font-semibold text-blue-900 text-sm">Dosage</span>
                </div>
                <p className="text-blue-800 font-medium">{result.dosage}</p>
              </div>

              {/* Crop */}
              <div className="bg-gradient-to-br from-emerald-50 to-emerald-100/60 rounded-xl p-4">
                <div className="flex items-center gap-2 mb-2">
                  <Sprout className="w-5 h-5 text-emerald-600" />
                  <span className="font-semibold text-emerald-900 text-sm">Target Crop</span>
                </div>
                <p className="text-emerald-800 font-medium">{result.crop}</p>
              </div>
            </div>

            {/* Instructions */}
            <div className="mt-4 bg-gradient-to-br from-gray-50 to-gray-100/60 rounded-xl p-4">
              <div className="flex items-center gap-2 mb-2">
                <Info className="w-5 h-5 text-gray-600" />
                <span className="font-semibold text-gray-800 text-sm">Application Instructions</span>
              </div>
              <p className="text-gray-700 leading-relaxed">{result.instructions}</p>
            </div>

            {!result.matched && (
              <div className="mt-4 flex items-start gap-2 text-yellow-700 bg-yellow-100 rounded-lg p-3 text-sm">
                <AlertCircle className="w-5 h-5 mt-0.5 shrink-0" />
                <span>
                  No exact match found in our database. The above is general guidance.
                  Please consult a local agriculture expert for specific advice.
                </span>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default PesticideRecommendation;
