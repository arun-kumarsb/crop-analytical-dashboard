import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Sprout, Droplets, Thermometer, Clock, ShieldCheck, Layers, ChevronRight, Activity } from 'lucide-react';
import { formatLargeNumber } from '../utils';

export default function CropIntelligenceView({ data, selectedCrop, onSelectCrop }) {
  const [activeCrop, setActiveCrop] = useState(selectedCrop || 'Wheat');
  const [activeStageIdx, setActiveStageIdx] = useState(0);
  const [searchFilter, setSearchFilter] = useState('');

  const allCrops = data.all_crops;
  const filteredCrops = allCrops.filter(c => c.toLowerCase().includes(searchFilter.toLowerCase()));

  const cp = data.crop_profiles[activeCrop] || {
    category: 'Cereal Grain',
    unit: 'Metric Tonnes',
    soils: ['Alluvial', 'Clay Loam'],
    water_req_mm: [450, 650],
    temp_range_c: [12, 25],
    season: 'Rabi',
    duration_days: [100, 140],
    stages: [],
    source: 'ICAR-IIWBR'
  };

  const stages = cp.stages || [];
  const currentStage = stages[activeStageIdx] || { stage: 'Germination', pct: 25, desc: 'Initial growth phase' };

  return (
    <div className="flex flex-col gap-5 w-full">
      {/* Top Crop Search & Selector Bar */}
      <div className="glass-panel p-5 flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
            <Sprout size={20} />
          </div>
          <div>
            <div className="text-xs font-bold uppercase tracking-wider text-slate-400 font-mono">
              CROP INTELLIGENCE & AGRONOMY
            </div>
            <div className="text-lg font-extrabold text-white flex items-center gap-2">
              <span>{activeCrop}</span>
              <span className="text-xs font-normal font-mono px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                {cp.category}
              </span>
            </div>
          </div>
        </div>

        {/* Search & Selector Input */}
        <div className="flex items-center gap-3">
          <input
            type="text"
            placeholder="Search 55 crops..."
            value={searchFilter}
            onChange={e => setSearchFilter(e.target.value)}
            className="bg-slate-900 border border-slate-700 text-xs font-mono rounded-xl px-3 py-2 text-white focus:outline-none focus:border-cyan-400 w-36 md:w-48"
          />
          <select
            value={activeCrop}
            onChange={e => {
              setActiveCrop(e.target.value);
              setActiveStageIdx(0);
              if (onSelectCrop) onSelectCrop(e.target.value);
            }}
            className="bg-slate-900 border border-slate-700 text-cyan-400 text-xs font-bold font-mono rounded-xl px-4 py-2 focus:outline-none focus:border-cyan-400"
          >
            {filteredCrops.map(c => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
        </div>
      </div>

      {/* 4 Agronomic Benchmark Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-5">
        <div className="glass-panel p-5">
          <div className="text-xs font-bold uppercase tracking-wider text-slate-400 font-mono flex items-center gap-1.5 mb-2">
            <Droplets size={14} className="text-cyan-400" /> WATER REQUIREMENT
          </div>
          <div className="text-2xl font-black font-mono text-cyan-400">
            {cp.water_req_mm[0]}–{cp.water_req_mm[1]} <span className="text-xs text-slate-400 font-normal">mm</span>
          </div>
          <div className="text-[11px] text-slate-400 mt-2">Optimal seasonal irrigation/rainfall</div>
        </div>

        <div className="glass-panel p-5">
          <div className="text-xs font-bold uppercase tracking-wider text-slate-400 font-mono flex items-center gap-1.5 mb-2">
            <Thermometer size={14} className="text-emerald-400" /> THERMAL OPTIMUM
          </div>
          <div className="text-2xl font-black font-mono text-emerald-400">
            {cp.temp_range_c[0]}–{cp.temp_range_c[1]} <span className="text-xs text-slate-400 font-normal">°C</span>
          </div>
          <div className="text-[11px] text-slate-400 mt-2">Vegetative and reproductive range</div>
        </div>

        <div className="glass-panel p-5">
          <div className="text-xs font-bold uppercase tracking-wider text-slate-400 font-mono flex items-center gap-1.5 mb-2">
            <Clock size={14} className="text-amber-400" /> MATURITY DURATION
          </div>
          <div className="text-2xl font-black font-mono text-amber-400">
            {cp.duration_days[0]}–{cp.duration_days[1]} <span className="text-xs text-slate-400 font-normal">days</span>
          </div>
          <div className="text-[11px] text-slate-400 mt-2">Sowing to physiological ripeness</div>
        </div>

        <div className="glass-panel p-5">
          <div className="text-xs font-bold uppercase tracking-wider text-slate-400 font-mono flex items-center gap-1.5 mb-2">
            <Layers size={14} className="text-blue-400" /> RECOMMENDED SOILS
          </div>
          <div className="text-xs font-bold text-white mt-1">
            {cp.soils.slice(0, 2).join(', ')}
          </div>
          <div className="text-[11px] text-slate-400 mt-2">Source: {cp.source}</div>
        </div>
      </div>

      {/* Interactive Step-by-Step Crop Lifecycle Visualizer */}
      <div className="glass-panel p-6">
        <div className="flex justify-between items-center mb-4">
          <div>
            <div className="text-xs font-bold uppercase tracking-wider text-cyan-400 font-mono flex items-center gap-1.5">
              <Activity size={14} /> CROP LIFECYCLE PROGRESSION // {activeCrop.toUpperCase()}
            </div>
            <div className="text-sm font-extrabold text-white">Stage-by-Stage Field Development & Care</div>
          </div>
          <span className="text-xs font-mono text-slate-400">
            Reporting Unit: <strong>{cp.unit}</strong>
          </span>
        </div>

        {/* Horizontal Stages Navigation Bar */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
          {stages.map((stg, idx) => {
            const isCurrent = activeStageIdx === idx;
            return (
              <button
                key={stg.stage}
                onClick={() => setActiveStageIdx(idx)}
                className={`p-3.5 rounded-xl border text-left transition-all relative overflow-hidden ${
                  isCurrent
                    ? 'bg-cyan-500/10 border-cyan-400/50 shadow-lg shadow-cyan-500/10'
                    : 'bg-slate-900/60 border-slate-800 hover:border-slate-700'
                }`}
              >
                <div className="flex justify-between items-center text-[10px] font-mono text-slate-400 mb-1">
                  <span>STAGE 0{idx + 1}</span>
                  <span className="text-cyan-400 font-bold">~{stg.pct}%</span>
                </div>
                <div className="font-bold text-xs text-white truncate">{stg.stage}</div>
                {isCurrent && (
                  <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-gradient-to-r from-cyan-400 to-emerald-400" />
                )}
              </button>
            );
          })}
        </div>

        {/* Active Stage Detailed Card */}
        <motion.div
          key={activeStageIdx}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-slate-900/80 border border-slate-700/60 rounded-2xl p-5"
        >
          <div className="flex items-center gap-2 mb-2">
            <span className="w-3 h-3 rounded-full bg-cyan-400 animate-pulse" />
            <h4 className="text-sm font-extrabold text-white">
              Stage {activeStageIdx + 1}: {currentStage.stage}
            </h4>
            <span className="text-[11px] font-mono px-2 py-0.5 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 ml-auto">
              Approx. {currentStage.pct}% of lifecycle
            </span>
          </div>
          <p className="text-sm text-slate-300 leading-relaxed">
            {currentStage.desc}
          </p>
        </motion.div>
      </div>
    </div>
  );
}
