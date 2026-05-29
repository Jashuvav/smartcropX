import React, { useState } from 'react';
import axios from 'axios';
import { API_URL } from '../config/api';
import {
  FlaskConical, Droplets, Leaf, Loader2, AlertCircle,
  ChevronDown, Search, Sprout, Trophy,
} from 'lucide-react';

const SOIL_TYPES = ['Alluvial', 'Black', 'Red', 'Laterite', 'Sandy', 'Clay', 'Loamy'];

const SoilRecommendation = () => {
  const [form, setForm] = useState({
    soil_type: 'Alluvial',
    ph: '',
    nitrogen: '',
    phosphorus: '',
    potassium: '',
  });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

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
        soil_type: form.soil_type,
        ph: parseFloat(form.ph),
        nitrogen: parseFloat(form.nitrogen),
        phosphorus: parseFloat(form.phosphorus),
        potassium: parseFloat(form.potassium),
      };
      const res = await axios.post(`${API_URL}/api/recommend/soil`, payload, { timeout: 10000 });
      setResult(res.data);
    } catch (err) {
      const msg = err.response?.data?.detail || err.message || 'Request failed';
      setError(typeof msg === 'string' ? msg : JSON.stringify(msg));
    } finally {
      setLoading(false);
    }
  };

  const barColor = (s) => {
    if (s >= 0.85) return 'from-green-500 to-emerald-400';
    if (s >= 0.7) return 'from-yellow-500 to-amber-400';
    return 'from-orange-500 to-red-400';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 pt-24 pb-16 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-10">
          <div className="inline-flex items-center gap-2 bg-amber-500/10 border border-amber-500/30 rounded-full px-4 py-1.5 mb-4">
            <FlaskConical size={16} className="text-amber-400" />
            <span className="text-amber-300 text-sm font-medium">Soil Suitability Analysis</span>
          </div>
          <h1 className="text-3xl md:text-4xl font-bold text-white mb-2">
            Soil-Based Crop Suitability
          </h1>
          <p className="text-gray-400 max-w-xl mx-auto">
            Enter your soil parameters and SmartCropX will rank the most suitable crops for your land.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Form */}
          <form onSubmit={handleSubmit} className="bg-gray-800/60 border border-gray-700 rounded-2xl p-6 space-y-5 h-fit">
            {/* Soil type */}
            <div>
              <label className="flex items-center gap-1.5 text-sm font-semibold text-gray-300 mb-2">
                <FlaskConical size={14} className="text-amber-400" /> Soil Type
              </label>
              <div className="relative">
                <select name="soil_type" value={form.soil_type} onChange={handleChange}
                  className="w-full appearance-none bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-sm text-white focus:ring-2 focus:ring-amber-500 outline-none pr-8">
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
                className="w-full bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-sm text-white placeholder-gray-500 focus:ring-2 focus:ring-amber-500 outline-none" required />
            </div>

            {/* NPK */}
            <div>
              <label className="flex items-center gap-1.5 text-sm font-semibold text-gray-300 mb-2">
                <Leaf size={14} className="text-green-400" /> NPK (kg/ha)
              </label>
              <div className="grid grid-cols-3 gap-3">
                <input name="nitrogen" value={form.nitrogen} onChange={handleChange} type="number" step="any" min="0" placeholder="N"
                  className="bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-sm text-white placeholder-gray-500 focus:ring-2 focus:ring-amber-500 outline-none" required />
                <input name="phosphorus" value={form.phosphorus} onChange={handleChange} type="number" step="any" min="0" placeholder="P"
                  className="bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-sm text-white placeholder-gray-500 focus:ring-2 focus:ring-amber-500 outline-none" required />
                <input name="potassium" value={form.potassium} onChange={handleChange} type="number" step="any" min="0" placeholder="K"
                  className="bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-sm text-white placeholder-gray-500 focus:ring-2 focus:ring-amber-500 outline-none" required />
              </div>
            </div>

            <button type="submit" disabled={loading}
              className="w-full bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-500 hover:to-orange-500 disabled:from-gray-700 disabled:to-gray-700 text-white font-semibold rounded-xl py-3 flex items-center justify-center gap-2 transition-all">
              {loading ? <><Loader2 size={18} className="animate-spin" /> Analysing…</> : <><Search size={18} /> Analyse Soil</>}
            </button>

            {error && (
              <div className="flex items-start gap-2 text-red-400 text-sm bg-red-500/10 border border-red-500/30 rounded-lg p-3">
                <AlertCircle size={16} className="mt-0.5 flex-shrink-0" /> {error}
              </div>
            )}
          </form>

          {/* Results */}
          <div className="space-y-4">
            {!result && !loading && (
              <div className="flex flex-col items-center justify-center text-gray-500 h-64">
                <Sprout size={48} className="mb-4 opacity-30" />
                <p className="text-lg text-center">Enter soil details and press <strong>Analyse Soil</strong></p>
              </div>
            )}

            {loading && (
              <div className="flex flex-col items-center justify-center h-64">
                <Loader2 size={40} className="animate-spin text-amber-400 mb-4" />
                <p className="text-gray-400">Ranking suitable crops…</p>
              </div>
            )}

            {result && (
              <>
                <h2 className="text-xl font-bold text-white flex items-center gap-2">
                  <Trophy size={20} className="text-amber-400" /> Top Suitable Crops
                </h2>
                {result.suitable_crops.map((crop, idx) => (
                  <div key={idx} className="bg-gray-800/60 border border-gray-700 rounded-xl p-4 hover:border-amber-600/50 transition-colors">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-3">
                        <span className="bg-amber-600/20 text-amber-400 text-xs font-bold w-7 h-7 rounded-full flex items-center justify-center">
                          #{idx + 1}
                        </span>
                        <h3 className="text-base font-bold text-white">{crop.crop}</h3>
                      </div>
                      <span className="text-xl font-extrabold text-amber-400">
                        {Math.round(crop.suitability * 100)}%
                      </span>
                    </div>
                    <div className="w-full h-2 bg-gray-700 rounded-full overflow-hidden">
                      <div className={`h-full rounded-full bg-gradient-to-r ${barColor(crop.suitability)} transition-all duration-700`}
                        style={{ width: `${crop.suitability * 100}%` }} />
                    </div>
                  </div>
                ))}
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SoilRecommendation;
