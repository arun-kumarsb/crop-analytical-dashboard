import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Swords, Droplets, Thermometer, Clock, ShieldCheck, Zap, Trophy, TrendingUp } from 'lucide-react';
import { ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';
import { formatLargeNumber } from '../utils';
import { playSwitchSound } from '../soundEffects';

export default function CropBattleView({ data }) {
  const [cropA, setCropA] = useState('Rice');
  const [cropB, setCropB] = useState('Bajra');

  const allCrops = data.all_crops;
  const pA = data.crop_profiles[cropA] || data.crop_profiles['Rice'];
  const pB = data.crop_profiles[cropB] || data.crop_profiles['Wheat'];

  const statsA = data.top_crops.find(c => c.Crop === cropA) || { production: 2229301180, yield_avg: 1.86 };
  const statsB = data.top_crops.find(c => c.Crop === cropB) || { production: 125000000, yield_avg: 1.15 };

  // Water savings calculation
  const meanWaterA = (pA.water_req_mm[0] + pA.water_req_mm[1]) / 2;
  const meanWaterB = (pB.water_req_mm[0] + pB.water_req_mm[1]) / 2;
  const waterDiffPct = Math.round(Math.abs((meanWaterA - meanWaterB) / Math.max(meanWaterA, meanWaterB)) * 100);
  const waterSaver = meanWaterA > meanWaterB ? cropB : cropA;

  // Radar comparison dataset
  const radarComparison = [
    {
      subject: 'Water Economy',
      A: Math.min(100, Math.round((1 - (meanWaterA / 2500)) * 100)),
      B: Math.min(100, Math.round((1 - (meanWaterB / 2500)) * 100))
    },
    {
      subject: 'Heat Resilience',
      A: Math.min(100, Math.round((pA.temp_range_c[1] / 45) * 100)),
      B: Math.min(100, Math.round((pB.temp_range_c[1] / 45) * 100))
    },
    {
      subject: 'Harvest Speed',
      A: Math.min(100, Math.round((1 - (pA.duration_days[0] / 365)) * 100)),
      B: Math.min(100, Math.round((1 - (pB.duration_days[0] / 365)) * 100))
    },
    {
      subject: 'Yield Potential',
      A: Math.min(100, Math.round(statsA.yield_avg * 20)),
      B: Math.min(100, Math.round(statsB.yield_avg * 20))
    },
    {
      subject: 'Soil Adaptability',
      A: pA.soils.length * 20,
      B: pB.soils.length * 20
    }
  ];

  return (
    <div className="flex flex-col gap-5 w-full">
      {/* Title Header */}
      <div className="glass-panel p-5 flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-400 to-blue-600 text-slate-950 font-black flex items-center justify-center text-xl shadow-lg shadow-cyan-500/20">
            ⚔️
          </div>
          <div>
            <div className="text-xs font-bold uppercase tracking-wider text-slate-400 font-mono">
              CLIMATE-SMART COMPARATOR
            </div>
            <div className="text-lg font-extrabold text-white flex items-center gap-2">
              <span>Head-to-Head Crop Battle</span>
              <span className="text-xs font-mono px-2 py-0.5 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/30">
                RESOURCE EFFICIENCY
              </span>
            </div>
          </div>
        </div>

        {/* Crop Selectors */}
        <div className="flex items-center gap-2">
          <select
            value={cropA}
            onChange={e => { setCropA(e.target.value); playSwitchSound(); }}
            className="bg-slate-900 border border-cyan-500/50 text-cyan-400 text-xs font-bold font-mono rounded-xl px-3 py-2"
          >
            {allCrops.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
          <span className="text-xs font-black text-slate-400 font-mono">VS</span>
          <select
            value={cropB}
            onChange={e => { setCropB(e.target.value); playSwitchSound(); }}
            className="bg-slate-900 border border-emerald-500/50 text-emerald-400 text-xs font-bold font-mono rounded-xl px-3 py-2"
          >
            {allCrops.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
        </div>
      </div>

      {/* Water Footprint & Climate Champion Banner */}
      <div className="glass-panel p-5 bg-gradient-to-r from-cyan-950/40 via-slate-900 to-emerald-950/40 border border-cyan-500/30">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-emerald-400">
              <Trophy size={18} />
            </div>
            <div>
              <div className="text-[11px] font-mono uppercase text-slate-400">WATER CONSERVATION CHAMPION</div>
              <div className="text-base font-extrabold text-emerald-400">
                {waterSaver} consumes {waterDiffPct}% LESS WATER than {waterSaver === cropA ? cropB : cropA}
              </div>
            </div>
          </div>
          <div className="text-xs font-mono text-slate-400 text-right">
            <span>UN Climate-Smart Agricultural Metric</span>
          </div>
        </div>
      </div>

      {/* Side-by-Side Comparison Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* Crop A Card (Left 4 cols) */}
        <div className="lg:col-span-4 glass-panel p-5 border-cyan-500/40 flex flex-col gap-4">
          <div className="flex justify-between items-center pb-3 border-b border-slate-800">
            <div>
              <span className="text-[10px] font-mono text-cyan-400 uppercase font-bold">CONTENDER A</span>
              <h3 className="text-xl font-black text-white">{cropA}</h3>
            </div>
            <span className="text-xs font-mono px-2 py-0.5 rounded-full bg-cyan-500/10 text-cyan-300 border border-cyan-500/30">
              {pA.category}
            </span>
          </div>

          <div className="space-y-3 text-xs font-mono">
            <div className="bg-slate-900/60 p-3 rounded-xl border border-slate-800 flex justify-between items-center">
              <span className="text-slate-400 flex items-center gap-1.5"><Droplets size={13} className="text-cyan-400" /> Water Need:</span>
              <span className="text-white font-bold">{pA.water_req_mm[0]}–{pA.water_req_mm[1]} mm</span>
            </div>
            <div className="bg-slate-900/60 p-3 rounded-xl border border-slate-800 flex justify-between items-center">
              <span className="text-slate-400 flex items-center gap-1.5"><Thermometer size={13} className="text-emerald-400" /> Optimal Temp:</span>
              <span className="text-white font-bold">{pA.temp_range_c[0]}–{pA.temp_range_c[1]} °C</span>
            </div>
            <div className="bg-slate-900/60 p-3 rounded-xl border border-slate-800 flex justify-between items-center">
              <span className="text-slate-400 flex items-center gap-1.5"><Clock size={13} className="text-amber-400" /> Harvest Duration:</span>
              <span className="text-white font-bold">{pA.duration_days[0]}–{pA.duration_days[1]} days</span>
            </div>
            <div className="bg-slate-900/60 p-3 rounded-xl border border-slate-800 flex justify-between items-center">
              <span className="text-slate-400 flex items-center gap-1.5"><TrendingUp size={13} className="text-blue-400" /> Historical Output:</span>
              <span className="text-cyan-400 font-bold">{formatLargeNumber(statsA.production)}</span>
            </div>
          </div>
        </div>

        {/* Radar Overlay (Center 4 cols) */}
        <div className="lg:col-span-4 glass-panel p-5 flex flex-col items-center justify-between">
          <div className="w-full text-center">
            <div className="text-xs font-mono uppercase font-bold text-slate-400">MULTIDIMENSIONAL OVERLAY</div>
            <div className="text-xs font-mono mt-1 flex justify-center gap-4">
              <span className="text-cyan-400">● {cropA}</span>
              <span className="text-emerald-400">● {cropB}</span>
            </div>
          </div>

          <div className="w-full h-56 flex items-center justify-center">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={radarComparison}>
                <PolarGrid stroke="#334155" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: '#94A3B8', fontSize: 9 }} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} stroke="#334155" />
                <Radar name={cropA} dataKey="A" stroke="#00E5FF" fill="#00E5FF" fillOpacity={0.2} strokeWidth={2} />
                <Radar name={cropB} dataKey="B" stroke="#00E676" fill="#00E676" fillOpacity={0.2} strokeWidth={2} />
              </RadarChart>
            </ResponsiveContainer>
          </div>

          <div className="text-[10px] text-slate-400 font-mono text-center">
            Higher values indicate greater sustainability & resource efficiency.
          </div>
        </div>

        {/* Crop B Card (Right 4 cols) */}
        <div className="lg:col-span-4 glass-panel p-5 border-emerald-500/40 flex flex-col gap-4">
          <div className="flex justify-between items-center pb-3 border-b border-slate-800">
            <div>
              <span className="text-[10px] font-mono text-emerald-400 uppercase font-bold">CONTENDER B</span>
              <h3 className="text-xl font-black text-white">{cropB}</h3>
            </div>
            <span className="text-xs font-mono px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-300 border border-emerald-500/30">
              {pB.category}
            </span>
          </div>

          <div className="space-y-3 text-xs font-mono">
            <div className="bg-slate-900/60 p-3 rounded-xl border border-slate-800 flex justify-between items-center">
              <span className="text-slate-400 flex items-center gap-1.5"><Droplets size={13} className="text-cyan-400" /> Water Need:</span>
              <span className="text-white font-bold">{pB.water_req_mm[0]}–{pB.water_req_mm[1]} mm</span>
            </div>
            <div className="bg-slate-900/60 p-3 rounded-xl border border-slate-800 flex justify-between items-center">
              <span className="text-slate-400 flex items-center gap-1.5"><Thermometer size={13} className="text-emerald-400" /> Optimal Temp:</span>
              <span className="text-white font-bold">{pB.temp_range_c[0]}–{pB.temp_range_c[1]} °C</span>
            </div>
            <div className="bg-slate-900/60 p-3 rounded-xl border border-slate-800 flex justify-between items-center">
              <span className="text-slate-400 flex items-center gap-1.5"><Clock size={13} className="text-amber-400" /> Harvest Duration:</span>
              <span className="text-white font-bold">{pB.duration_days[0]}–{pB.duration_days[1]} days</span>
            </div>
            <div className="bg-slate-900/60 p-3 rounded-xl border border-slate-800 flex justify-between items-center">
              <span className="text-slate-400 flex items-center gap-1.5"><TrendingUp size={13} className="text-blue-400" /> Historical Output:</span>
              <span className="text-emerald-400 font-bold">{formatLargeNumber(statsB.production)}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
