import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { API_URL } from '../config/api';
import {
  MapPin, Droplets, FlaskConical, Leaf, CloudRain,
  Thermometer, BarChart3, Loader2, AlertCircle, Sprout, Satellite,
  ChevronDown, Search,
} from 'lucide-react';

const SOIL_TYPES = ['Alluvial', 'Black', 'Red', 'Laterite', 'Sandy', 'Clay', 'Loamy'];

const CropRecommendation = () => {
  const [form, setForm] = useState({
    latitude: '',
    longitude: '',
    district: '',
    soil_type: 'Alluvial',
    ph: '',
    nitrogen: '',
    phosphorus: '',
    potassium: '',
  });
  const [loading, setLoading] = useState(false);
  const [locLoading, setLocLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  /* ── auto-detect location ── */
  const detectLocation = useCallback(() => {
    if (!navigator.geolocation) {
      setError('Geolocation is not supported by your browser');
      return;
    }
    setLocLoading(true);
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setForm((f) => ({
          ...f,
          latitude: pos.coords.latitude.toFixed(4),
          longitude: pos.coords.longitude.toFixed(4),
        }));
        setLocLoading(false);
      },
      () => {
        setError('Unable to detect location. Please enter manually.');
        setLocLoading(false);
      },
      { timeout: 10000 },
    );
  }, []);

  useEffect(() => {
    detectLocation();
  }, [detectLocation]);

  /* ── handlers ── */
  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((f) => ({ ...f, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setResult(null);
    setLoading(true);
    try {
      const payload = {
        latitude: parseFloat(form.latitude),
        longitude: parseFloat(form.longitude),
        district: form.district || undefined,
        soil_type: form.soil_type,
        ph: parseFloat(form.ph),
        nitrogen: parseFloat(form.nitrogen),
        phosphorus: parseFloat(form.phosphorus),
        potassium: parseFloat(form.potassium),
      };
      const res = await axios.post(`${API_URL}/api/recommend/crop`, payload, { timeout: 15000 });
      setResult(res.data);
    } catch (err) {
      const msg = err.response?.data?.detail || err.message || 'Request failed';
      setError(typeof msg === 'string' ? msg : JSON.stringify(msg));
    } finally {
      setLoading(false);
    }
  };

  /* ── NDVI colour helper ── */
  const ndviColor = (v) => {
    if (v >= 0.6) return 'bg-green-500';
    if (v >= 0.4) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  /* ── score colour ── */
  const scoreColor = (s) => {
    if (s >= 0.75) return 'text-green-400';
    if (s >= 0.5) return 'text-yellow-400';
    return 'text-red-400';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 pt-24 pb-16 px-4">
      <div className="max-w-5xl mx-auto">
        {/* ── Header ── */}
        <div className="text-center mb-10">
          <div className="inline-flex items-center gap-2 bg-green-500/10 border border-green-500/30 rounded-full px-4 py-1.5 mb-4">
            <Sprout size={16} className="text-green-400" />
            <span className="text-green-300 text-sm font-medium">AI-Powered Crop Recommendation</span>
          </div>
          <h1 className="text-3xl md:text-4xl font-bold text-white mb-2">
            Crop Recommendation Engine
          </h1>
          <p className="text-gray-400 max-w-xl mx-auto">
            Enter your location and soil parameters below. SmartCropX will analyse weather,
            satellite NDVI, and soil data to suggest the best crops for you.
          </p>
        </div>

        <div className="grid lg:grid-cols-5 gap-8">
          {/* ── Form (left 2 cols) ── */}
          <form onSubmit={handleSubmit} className="lg:col-span-2 bg-gray-800/60 border border-gray-700 rounded-2xl p-6 space-y-5 h-fit">
            {/* Location */}
            <div>
              <label className="flex items-center gap-1.5 text-sm font-semibold text-gray-300 mb-2">
                <MapPin size={14} className="text-green-400" /> Location
              </label>
              <div className="grid grid-cols-2 gap-3">
                <input name="latitude" value={form.latitude} onChange={handleChange} type="number" step="any" placeholder="Latitude"
                  className="bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-sm text-white placeholder-gray-500 focus:ring-2 focus:ring-green-500 outline-none" required />
                <input name="longitude" value={form.longitude} onChange={handleChange} type="number" step="any" placeholder="Longitude"
                  className="bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-sm text-white placeholder-gray-500 focus:ring-2 focus:ring-green-500 outline-none" required />
              </div>
              <button type="button" onClick={detectLocation} disabled={locLoading}
                className="mt-2 text-xs text-green-400 hover:text-green-300 flex items-center gap-1">
                {locLoading ? <Loader2 size={12} className="animate-spin" /> : <MapPin size={12} />}
                {locLoading ? 'Detecting…' : 'Auto-detect my location'}
              </button>
              <input name="district" value={form.district} onChange={handleChange} placeholder="District / town (optional)"
                className="mt-2 w-full bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-sm text-white placeholder-gray-500 focus:ring-2 focus:ring-green-500 outline-none" />
            </div>

            {/* Soil type */}
            <div>
              <label className="flex items-center gap-1.5 text-sm font-semibold text-gray-300 mb-2">
                <FlaskConical size={14} className="text-amber-400" /> Soil Type
              </label>
              <div className="relative">
                <select name="soil_type" value={form.soil_type} onChange={handleChange}
                  className="w-full appearance-none bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-sm text-white focus:ring-2 focus:ring-green-500 outline-none pr-8">
                  {SOIL_TYPES.map((s) => <option key={s} value={s}>{s}</option>)}
                </select>
                <ChevronDown size={14} className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 pointer-events-none" />
              </div>
            </div>

            {/* pH */}
            <div>
              <label className="flex items-center gap-1.5 text-sm font-semibold text-gray-300 mb-2">
                <Droplets size={14} className="text-blue-400" /> Soil pH
              </label>
              <input name="ph" value={form.ph} onChange={handleChange} type="number" step="0.1" min="0" max="14" placeholder="e.g. 6.5"
                className="w-full bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-sm text-white placeholder-gray-500 focus:ring-2 focus:ring-green-500 outline-none" required />
            </div>

            {/* NPK */}
            <div>
              <label className="flex items-center gap-1.5 text-sm font-semibold text-gray-300 mb-2">
                <Leaf size={14} className="text-green-400" /> NPK (kg/ha)
              </label>
              <div className="grid grid-cols-3 gap-3">
                <input name="nitrogen" value={form.nitrogen} onChange={handleChange} type="number" step="any" min="0" placeholder="N"
                  className="bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-sm text-white placeholder-gray-500 focus:ring-2 focus:ring-green-500 outline-none" required />
                <input name="phosphorus" value={form.phosphorus} onChange={handleChange} type="number" step="any" min="0" placeholder="P"
                  className="bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-sm text-white placeholder-gray-500 focus:ring-2 focus:ring-green-500 outline-none" required />
                <input name="potassium" value={form.potassium} onChange={handleChange} type="number" step="any" min="0" placeholder="K"
                  className="bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-sm text-white placeholder-gray-500 focus:ring-2 focus:ring-green-500 outline-none" required />
              </div>
            </div>

            {/* Submit */}
            <button type="submit" disabled={loading}
              className="w-full bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-500 hover:to-emerald-500 disabled:from-gray-700 disabled:to-gray-700 text-white font-semibold rounded-xl py-3 flex items-center justify-center gap-2 transition-all">
              {loading ? <><Loader2 size={18} className="animate-spin" /> Analysing…</> : <><Search size={18} /> Get Recommendations</>}
            </button>

            {error && (
              <div className="flex items-start gap-2 text-red-400 text-sm bg-red-500/10 border border-red-500/30 rounded-lg p-3">
                <AlertCircle size={16} className="mt-0.5 flex-shrink-0" /> {error}
              </div>
            )}
          </form>

          {/* ── Results (right 3 cols) ── */}
          <div className="lg:col-span-3 space-y-6">
            {!result && !loading && (
              <div className="flex flex-col items-center justify-center text-gray-500 h-64">
                <Sprout size={48} className="mb-4 opacity-30" />
                <p className="text-lg">Fill the form and press <strong>Get Recommendations</strong></p>
              </div>
            )}

            {loading && (
              <div className="flex flex-col items-center justify-center h-64">
                <Loader2 size={40} className="animate-spin text-green-400 mb-4" />
                <p className="text-gray-400">Fetching weather, satellite data & scoring crops…</p>
              </div>
            )}

            {result && (
              <>
                {/* Weather & NDVI summary */}
                <div className="grid sm:grid-cols-4 gap-4">
                  <SummaryCard icon={<Thermometer size={20} />} label="Temperature" value={`${result.weather_summary.temperature_c}°C`} color="text-orange-400" />
                  <SummaryCard icon={<CloudRain size={20} />} label="Rainfall (7d)" value={`${result.weather_summary.rainfall_mm} mm`} color="text-blue-400" />
                  <SummaryCard icon={<Droplets size={20} />} label="Humidity" value={`${result.weather_summary.humidity_pct}%`} color="text-cyan-400" />
                  <div className="bg-gray-800/60 border border-gray-700 rounded-xl p-4 flex flex-col items-center">
                    <Satellite size={20} className="text-purple-400 mb-1" />
                    <span className="text-[11px] text-gray-500 uppercase tracking-wider">NDVI</span>
                    <span className="text-lg font-bold text-white">{result.ndvi}</span>
                    <div className="w-full h-2 bg-gray-700 rounded-full mt-2 overflow-hidden">
                      <div className={`h-full rounded-full ${ndviColor(result.ndvi)}`} style={{ width: `${result.ndvi * 100}%` }} />
                    </div>
                  </div>
                </div>

                {result.weather_summary.source === 'fallback-demo' && (
                  <div className="text-xs text-yellow-400 bg-yellow-500/10 border border-yellow-500/30 rounded-lg px-3 py-2 flex items-center gap-2">
                    <AlertCircle size={14} /> Weather API unreachable — using demo values.
                  </div>
                )}

                {/* Top crops */}
                <h2 className="text-xl font-bold text-white flex items-center gap-2">
                  <BarChart3 size={20} className="text-green-400" /> Top Recommended Crops
                </h2>

                <div className="space-y-4">
                  {result.recommended_crops.map((crop, idx) => (
                    <div key={idx} className="bg-gray-800/60 border border-gray-700 rounded-xl p-5 hover:border-green-600/50 transition-colors">
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center gap-3">
                          <span className="bg-green-600/20 text-green-400 text-xs font-bold w-7 h-7 rounded-full flex items-center justify-center">
                            #{idx + 1}
                          </span>
                          <h3 className="text-lg font-bold text-white">{crop.crop}</h3>
                        </div>
                        <span className={`text-2xl font-extrabold ${scoreColor(crop.score)}`}>
                          {Math.round(crop.score * 100)}%
                        </span>
                      </div>
                      {/* Score bar */}
                      <div className="w-full h-2 bg-gray-700 rounded-full mb-3 overflow-hidden">
                        <div className="h-full rounded-full bg-gradient-to-r from-green-500 to-emerald-400 transition-all duration-700"
                          style={{ width: `${crop.score * 100}%` }} />
                      </div>
                      {/* Reason bullets */}
                      <div className="flex flex-wrap gap-2">
                        {crop.reason.split(' • ').map((r, i) => (
                          <span key={i} className="text-[11px] bg-gray-700/60 text-gray-300 rounded-full px-2.5 py-0.5">{r}</span>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

/* ── helper component ── */
const SummaryCard = ({ icon, label, value, color }) => (
  <div className="bg-gray-800/60 border border-gray-700 rounded-xl p-4 flex flex-col items-center">
    <span className={color}>{icon}</span>
    <span className="text-[11px] text-gray-500 uppercase tracking-wider mt-1">{label}</span>
    <span className="text-lg font-bold text-white">{value}</span>
  </div>
);

export default CropRecommendation;
