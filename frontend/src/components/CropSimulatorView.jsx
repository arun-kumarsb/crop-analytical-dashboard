import React, { useState, useMemo } from 'react';
import { motion } from 'framer-motion';
import confetti from 'canvas-confetti';
import { Sparkles, Sliders, AlertTriangle, CheckCircle2, Droplets, Thermometer, Layers, Compass, ArrowRight } from 'lucide-react';
import { playSuccessChord, playClickSound } from '../soundEffects';

export default function CropSimulatorView({ data, onSelectCrop }) {
  const [selectedState, setSelectedState] = useState('Punjab');
  const [selectedSoil, setSelectedSoil] = useState('Alluvial Loam');
  const [waterAvailable, setWaterAvailable] = useState(650);
  const [tempEstimate, setTempEstimate] = useState(24);
  const [season, setSeason] = useState('Rabi');

  const allStates = data.all_states;
  const soilOptions = [
    'Alluvial Loam',
    'Black Cotton Soil (Regur)',
    'Deep Sandy Loam',
    'Red Sandy Loam',
    'Laterite Soil',
    'Clay Loam',
    'Mountainous Forest Soil'
  ];

  // Algorithmic Agronomic Matching
  const recommendations = useMemo(() => {
    const list = Object.entries(data.crop_profiles).map(([cropName, p]) => {
      // 1. Water Match Score (0 - 40 pts)
      const [wMin, wMax] = p.water_req_mm;
      let waterScore = 0;
      if (waterAvailable >= wMin && waterAvailable <= wMax) {
        waterScore = 40;
      } else if (waterAvailable < wMin) {
        const def = wMin - waterAvailable;
        waterScore = Math.max(0, 40 - (def / wMin) * 50);
      } else {
        const excess = waterAvailable - wMax;
        waterScore = Math.max(10, 40 - (excess / wMax) * 25);
      }

      // 2. Temperature Match Score (0 - 30 pts)
      const [tMin, tMax] = p.temp_range_c;
      let tempScore = 0;
      if (tempEstimate >= tMin && tempEstimate <= tMax) {
        tempScore = 30;
      } else if (tempEstimate < tMin) {
        tempScore = Math.max(0, 30 - (tMin - tempEstimate) * 4);
      } else {
        tempScore = Math.max(0, 30 - (tempEstimate - tMax) * 4);
      }

      // 3. Soil Match Score (0 - 30 pts)
      let soilScore = 15;
      const cleanSoil = selectedSoil.toLowerCase();
      const hasDirectSoil = p.soils.some(s => s.toLowerCase().includes(cleanSoil) || cleanSoil.includes(s.toLowerCase()));
      if (hasDirectSoil) {
        soilScore = 30;
      } else if (cleanSoil.includes('loam')) {
        soilScore = 22;
      }

      const totalScore = Math.min(100, Math.round(waterScore + tempScore + soilScore));

      return {
        crop: cropName,
        score: totalScore,
        category: p.category,
        waterReq: `${wMin}–${wMax} mm`,
        tempReq: `${tMin}–${tMax} °C`,
        soils: p.soils,
        duration: `${p.duration_days[0]}–${p.duration_days[1]} days`,
        source: p.source,
        waterDeficit: waterAvailable < wMin ? wMin - waterAvailable : 0
      };
    });

    return list.sort((a, b) => b.score - a.score);
  }, [data.crop_profiles, selectedSoil, waterAvailable, tempEstimate]);

  const topMatches = recommendations.slice(0, 3);
  const highRiskCrops = recommendations.slice(-3).reverse();

  const handleSimulate = () => {
    playSuccessChord();
    confetti({
      particleCount: 60,
      spread: 70,
      origin: { y: 0.6 }
    });
  };

  return (
    <div className="flex flex-col gap-5 w-full">
      {/* Title Header */}
      <div className="glass-panel p-5 flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-400 to-emerald-500 text-slate-950 font-black flex items-center justify-center text-xl shadow-lg shadow-cyan-500/20">
            🔮
          </div>
          <div>
            <div className="text-xs font-bold uppercase tracking-wider text-slate-400 font-mono">
              PREDICTIVE DECISION SUPPORT ENGINE
            </div>
            <div className="text-lg font-extrabold text-white flex items-center gap-2">
              <span>Crop Recommendation & Feasibility Simulator</span>
              <span className="text-xs font-mono px-2 py-0.5 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/30">
                ICAR ALGORITHMIC MODEL
              </span>
            </div>
          </div>
        </div>

        <button
          onClick={handleSimulate}
          className="px-4 py-2 rounded-xl bg-gradient-to-r from-cyan-500 to-emerald-400 hover:from-cyan-400 hover:to-emerald-300 text-slate-950 font-bold text-xs flex items-center gap-2 shadow-lg shadow-cyan-500/20 transition-all font-mono"
        >
          <Sparkles size={14} />
          <span>Run Simulation</span>
        </button>
      </div>

      {/* Main Grid: Controls (Left 4 cols) & Results (Right 8 cols) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 w-full">
        {/* Controls Panel */}
        <div className="lg:col-span-4 glass-panel p-6 flex flex-col gap-4">
          <div className="text-xs font-bold uppercase tracking-wider text-cyan-400 font-mono flex items-center gap-1.5 mb-1">
            <Sliders size={14} /> FIELD CONDITIONS INPUT
          </div>

          {/* Region */}
          <div>
            <label className="text-xs font-semibold text-slate-300 mb-1.5 block">Target Indian State</label>
            <select
              value={selectedState}
              onChange={e => { setSelectedState(e.target.value); playClickSound(); }}
              className="w-full bg-slate-900 border border-slate-700 text-cyan-400 text-xs font-mono font-bold rounded-xl px-3.5 py-2.5 focus:outline-none focus:border-cyan-400"
            >
              {allStates.map(s => <option key={s} value={s}>{s}</option>)}
            </select>
          </div>

          {/* Soil Type */}
          <div>
            <label className="text-xs font-semibold text-slate-300 mb-1.5 block">Soil Classification</label>
            <select
              value={selectedSoil}
              onChange={e => { setSelectedSoil(e.target.value); playClickSound(); }}
              className="w-full bg-slate-900 border border-slate-700 text-amber-300 text-xs font-mono font-bold rounded-xl px-3.5 py-2.5 focus:outline-none focus:border-cyan-400"
            >
              {soilOptions.map(s => <option key={s} value={s}>{s}</option>)}
            </select>
          </div>

          {/* Available Water / Rainfall Slider */}
          <div>
            <div className="flex justify-between items-center text-xs mb-1.5">
              <span className="font-semibold text-slate-300">Available Water Supply</span>
              <span className="font-mono text-cyan-400 font-bold">{waterAvailable} mm</span>
            </div>
            <input
              type="range"
              min={250}
              max={2200}
              step={25}
              value={waterAvailable}
              onChange={e => setWaterAvailable(Number(e.target.value))}
              className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-cyan-400"
            />
            <div className="flex justify-between text-[10px] text-slate-500 font-mono mt-1">
              <span>Arid (250 mm)</span>
              <span>Monsoon (1200 mm)</span>
              <span>Delta (2200 mm)</span>
            </div>
          </div>

          {/* Mean Temperature Slider */}
          <div>
            <div className="flex justify-between items-center text-xs mb-1.5">
              <span className="font-semibold text-slate-300">Mean Growing Season Temp</span>
              <span className="font-mono text-emerald-400 font-bold">{tempEstimate} °C</span>
            </div>
            <input
              type="range"
              min={12}
              max={40}
              step={1}
              value={tempEstimate}
              onChange={e => setTempEstimate(Number(e.target.value))}
              className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-emerald-400"
            />
            <div className="flex justify-between text-[10px] text-slate-500 font-mono mt-1">
              <span>Cool Rabi (12°C)</span>
              <span>Temperate (25°C)</span>
              <span>Hot Kharif (40°C)</span>
            </div>
          </div>

          {/* Season Radio Pills */}
          <div>
            <label className="text-xs font-semibold text-slate-300 mb-1.5 block">Cultivation Season</label>
            <div className="flex gap-2">
              {['Kharif', 'Rabi', 'Whole Year'].map(s => (
                <button
                  key={s}
                  onClick={() => { setSeason(s); playClickSound(); }}
                  className={`flex-1 py-1.5 rounded-xl text-xs font-mono font-bold transition-all ${
                    season === s
                      ? 'bg-cyan-500 text-slate-950 shadow-md shadow-cyan-500/20'
                      : 'bg-slate-900 border border-slate-700 text-slate-400 hover:text-slate-200'
                  }`}
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Results Panel */}
        <div className="lg:col-span-8 flex flex-col gap-5">
          {/* Hero Match: Top Recommendation */}
          {topMatches[0] && (
            <motion.div
              key={topMatches[0].crop}
              initial={{ opacity: 0, scale: 0.98 }}
              animate={{ opacity: 1, scale: 1 }}
              className="glass-panel p-6 border-cyan-400/50 bg-gradient-to-br from-slate-900 via-slate-900 to-cyan-950/40 relative overflow-hidden shadow-2xl"
            >
              <div className="absolute top-0 right-0 w-32 h-32 bg-cyan-400/10 rounded-full blur-2xl pointer-events-none" />

              <div className="flex flex-wrap justify-between items-center gap-3 mb-3">
                <span className="text-xs font-mono uppercase font-bold text-cyan-400 tracking-wider flex items-center gap-1.5">
                  <CheckCircle2 size={15} /> 🥇 TOP FEASIBILITY RECOMMENDATION
                </span>
                <span className="px-3 py-1 rounded-full bg-cyan-400 text-slate-950 font-black font-mono text-sm shadow-md shadow-cyan-400/30">
                  {topMatches[0].score}% MATCH
                </span>
              </div>

              <div className="text-2xl font-black text-white mb-2 flex items-center gap-2">
                <span>{topMatches[0].crop}</span>
                <span className="text-xs font-mono font-medium px-2.5 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
                  {topMatches[0].category}
                </span>
              </div>

              <p className="text-xs text-slate-300 leading-relaxed mb-4">
                Under <strong>{selectedSoil}</strong> with <strong>{waterAvailable} mm</strong> water and <strong>{tempEstimate}°C</strong>,{' '}
                <strong>{topMatches[0].crop}</strong> achieves near-optimal agronomic balance with minimal environmental stress.
              </p>

              {/* Benchmark Grid */}
              <div className="grid grid-cols-3 gap-3 bg-slate-950/60 rounded-xl p-3 border border-slate-800 text-xs font-mono">
                <div>
                  <div className="text-slate-400 text-[10px]">WATER NEED</div>
                  <div className="text-cyan-400 font-bold">{topMatches[0].waterReq}</div>
                </div>
                <div>
                  <div className="text-slate-400 text-[10px]">THERMAL FIT</div>
                  <div className="text-emerald-400 font-bold">{topMatches[0].tempReq}</div>
                </div>
                <div>
                  <div className="text-slate-400 text-[10px]">HARVEST CYCLE</div>
                  <div className="text-amber-400 font-bold">{topMatches[0].duration}</div>
                </div>
              </div>
            </motion.div>
          )}

          {/* Secondary Matches Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {topMatches.slice(1, 3).map((match, idx) => (
              <div key={match.crop} className="glass-panel p-4 flex flex-col justify-between">
                <div>
                  <div className="flex justify-between items-center text-xs font-mono mb-1">
                    <span className="text-slate-400">#{idx + 2} VIABLE ALTERNATIVE</span>
                    <span className="text-emerald-400 font-bold">{match.score}%</span>
                  </div>
                  <div className="font-bold text-base text-white mb-1">{match.crop}</div>
                  <div className="text-[11px] text-slate-400 mb-3">{match.category} • {match.waterReq}</div>
                </div>
                <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                  <div className="h-full bg-emerald-400 rounded-full" style={{ width: `${match.score}%` }} />
                </div>
              </div>
            ))}
          </div>

          {/* High Risk / Infeasible Crops Alert Box */}
          <div className="glass-panel p-5 border-red-500/30 bg-gradient-to-br from-slate-900 to-red-950/20">
            <div className="text-xs font-bold uppercase text-red-400 font-mono flex items-center gap-1.5 mb-2">
              <AlertTriangle size={15} /> HIGH-RISK / INCOMPATIBLE CROPS (ACUTE DEFICIT WARNING)
            </div>
            <p className="text-xs text-slate-300 leading-relaxed mb-3">
              The following crops are statistically unviable under your selected parameters without massive artificial irrigation:
            </p>
            <div className="flex flex-wrap gap-2">
              {highRiskCrops.map(c => (
                <span
                  key={c.crop}
                  className="px-3 py-1 rounded-xl bg-red-500/10 border border-red-500/30 text-red-300 text-xs font-mono font-semibold"
                >
                  ⚠️ {c.crop} ({c.score}% Match — Needs {c.waterReq})
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
