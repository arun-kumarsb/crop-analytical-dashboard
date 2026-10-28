import React, { useState } from 'react';
import { motion } from 'framer-motion';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, AreaChart, Area, RadarChart, Radar, PolarGrid,
  PolarAngleAxis, PolarRadiusAxis
} from 'recharts';
import { formatLargeNumber, formatExact } from '../utils';
import { TrendingUp, ArrowUpRight, Zap, Target, Layers, Droplets } from 'lucide-react';

export default function DashboardView({ data, activeYear, excludeCoconut }) {
  const [inflowFilter, setInflowFilter] = useState('All');
  const kpis = data.kpis;

  // Filter yearly or full production
  const displayProd = activeYear === 'All'
    ? kpis.total_production
    : (data.yearly.find(y => String(y.Crop_Year) === String(activeYear))?.production || kpis.total_production);

  const displayArea = activeYear === 'All'
    ? kpis.total_area
    : (data.yearly.find(y => String(y.Crop_Year) === String(activeYear))?.area || kpis.total_area);

  // Left Column: Top 4 Crops Targets
  const top4Crops = data.top_crops.slice(0, 4);

  // Center Column: Yearly Inflow Bars
  const yearlyChartData = data.yearly.map(y => ({
    year: String(y.Crop_Year),
    production: y.production,
    isPeak: y.production === Math.max(...data.yearly.map(m => m.production)),
    isActive: String(y.Crop_Year) === String(activeYear),
  }));

  // Center Column: Donut Categories
  const categoryData = data.categories.slice(0, 5).map(c => ({
    name: c.Category,
    value: c.production,
    share: c.share_pct,
  }));
  const CAT_COLORS = ['#00E5FF', '#00E676', '#2979FF', '#FFB300', '#A855F7'];

  // Bottom Center: Rainfall vs Yield Spline Wave
  const waveData = data.yearly.map(y => ({
    year: String(y.Crop_Year),
    rainfall: Math.round(y.rainfall),
    yieldIndex: Number((y.yield_avg * 10).toFixed(1)),
  }));

  // Right Column: Radar Data (Agronomic Structure)
  const radarData = [
    { subject: 'Yield Index', A: 88, fullMark: 100 },
    { subject: 'Rainfall Fit', A: 78, fullMark: 100 },
    { subject: 'Acreage', A: 94, fullMark: 100 },
    { subject: 'Soil Quality', A: 85, fullMark: 100 },
    { subject: 'Crop Variety', A: 76, fullMark: 100 },
  ];

  // Right Column: Regional Donut
  const topStatesDonut = data.states.slice(0, 5).map(s => ({
    name: s.State,
    value: s.production,
    share: s.share_pct,
  }));
  const STATE_COLORS = ['#00E676', '#00E5FF', '#2979FF', '#8B5CF6', '#F59E0B'];

  // Right Column Bottom: Milestones
  const milestoneData = data.milestones.map(m => ({
    year: String(m.Crop_Year),
    production: m.production,
  }));

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 w-full">
      {/* ==================================================================== */}
      {/* LEFT COLUMN (Cols: 3 / 12) - Cards 1 & 2                             */}
      {/* ==================================================================== */}
      <div className="lg:col-span-3 flex flex-col gap-5">
        {/* Card 1: Credit Card Style KPI */}
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          className="relative rounded-[22px] p-6 text-white overflow-hidden shadow-2xl shadow-cyan-950/40 border border-cyan-400/30 bg-gradient-to-br from-[#0A192F] via-[#0F3460] to-[#16213E] group hover:border-cyan-400/60 transition-all"
        >
          {/* Ambient radial glow */}
          <div className="absolute -top-12 -right-12 w-40 h-40 bg-cyan-400/20 rounded-full blur-2xl pointer-events-none group-hover:bg-cyan-400/30 transition-all" />

          {/* Card Top Row */}
          <div className="flex justify-between items-center mb-4">
            <span className="text-[11px] font-bold tracking-widest text-cyan-200 uppercase font-mono flex items-center gap-1.5">
              <Zap size={13} className="text-cyan-400" />
              {excludeCoconut ? 'HARVEST (TONNES ONLY)' : 'CUMULATIVE OUTPUT'}
            </span>
            <span className="text-[11px] px-2.5 py-0.5 rounded-full bg-white/10 border border-white/20 font-mono">
              IND // {activeYear}
            </span>
          </div>

          {/* Big KPI Value */}
          <div className="text-3xl font-black font-mono tracking-tight text-white mb-1">
            {formatLargeNumber(displayProd)} <span className="text-xs font-normal text-cyan-300 font-sans">{excludeCoconut ? 'Metric Tonnes' : 'Units'}</span>
          </div>
          <div className="text-xs text-cyan-200/80 mb-5 flex items-center justify-between">
            <span>Acreage: <strong>{formatLargeNumber(displayArea)}</strong></span>
            <span className="flex items-center gap-1 text-emerald-400 font-bold">
              <ArrowUpRight size={13} /> +4.2%
            </span>
          </div>

          {/* Circular Gauge / Sub-metric Box */}
          <div className="flex items-center justify-between bg-slate-950/40 rounded-xl p-3 border border-white/10 backdrop-blur-md">
            <div>
              <div className="text-[10px] uppercase font-bold text-slate-400">Mean Harvest Yield</div>
              <div className="text-lg font-black font-mono text-cyan-400">
                {kpis.avg_yield.toFixed(2)} <span className="text-xs font-normal text-slate-400">t/ha</span>
              </div>
            </div>
            {/* Circular Ring Gauge */}
            <div className="relative w-12 h-12 flex items-center justify-center">
              <svg className="w-12 h-12 transform -rotate-90">
                <circle cx="24" cy="24" r="18" stroke="currentColor" strokeWidth="3" className="text-slate-800" fill="transparent" />
                <circle cx="24" cy="24" r="18" stroke="currentColor" strokeWidth="3" strokeDasharray="113" strokeDashoffset="14" strokeLinecap="round" className="text-cyan-400" fill="transparent" />
              </svg>
              <span className="absolute text-[11px] font-bold font-mono text-cyan-300">88%</span>
            </div>
          </div>
        </motion.div>

        {/* Card 2: Goals / Top Crop Performance Targets */}
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="glass-panel p-5 flex flex-col justify-between"
        >
          <div className="flex justify-between items-center mb-4">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
              <Target size={14} className="text-cyan-400" />
              COMMODITY TARGETS
            </span>
            <span className="text-[11px] font-mono text-cyan-400 font-bold">SHARE %</span>
          </div>

          <div className="flex flex-col gap-3.5">
            {top4Crops.map((crop, idx) => {
              const targetPct = Math.min(100, Math.round(crop.share_pct * 3.2));
              return (
                <div key={crop.Crop} className="flex flex-col gap-1.5">
                  <div className="flex justify-between items-center text-xs">
                    <span className="font-semibold text-slate-200 flex items-center gap-2">
                      <span className="w-2 h-2 rounded-full bg-cyan-400" />
                      {crop.Crop}
                    </span>
                    <span className="font-mono text-cyan-400 font-bold text-[11px]">
                      {formatLargeNumber(crop.production)}
                    </span>
                  </div>
                  <div className="w-full bg-slate-800/80 rounded-full h-2 overflow-hidden">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${targetPct}%` }}
                      transition={{ duration: 1, delay: idx * 0.1 }}
                      className="h-full rounded-full bg-gradient-to-r from-blue-500 via-cyan-400 to-emerald-400 shadow-sm shadow-cyan-400/30"
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </motion.div>
      </div>

      {/* ==================================================================== */}
      {/* CENTER COLUMN (Cols: 5 / 12) - Cards 3, 4 & 5                        */}
      {/* ==================================================================== */}
      <div className="lg:col-span-5 flex flex-col gap-5">
        {/* Card 3: Inflow / Historical Production Bar Chart */}
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.15 }}
          className="glass-panel p-5"
        >
          <div className="flex justify-between items-center mb-2">
            <div>
              <div className="text-xs font-bold uppercase tracking-wider text-slate-400">Production Trend</div>
              <div className="text-sm font-extrabold text-white">Historical Volume Breakdown</div>
            </div>
            <div className="text-right">
              <span className="text-[10px] uppercase font-mono px-2 py-0.5 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/30">
                Peak: 2019
              </span>
              <div className="text-base font-black font-mono text-cyan-400">
                {formatLargeNumber(Math.max(...data.yearly.map(m => m.production)))}
              </div>
            </div>
          </div>

          <div className="w-full h-44">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={yearlyChartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <XAxis dataKey="year" stroke="#64748B" fontSize={10} tickLine={false} interval={3} />
                <YAxis stroke="#64748B" fontSize={10} tickLine={false} tickFormatter={formatLargeNumber} />
                <Tooltip
                  cursor={{ fill: 'rgba(0, 229, 255, 0.05)' }}
                  content={({ active, payload }) => {
                    if (active && payload && payload.length) {
                      return (
                        <div className="bg-slate-900/90 border border-cyan-500/40 p-2.5 rounded-xl shadow-xl text-xs font-mono">
                          <div className="text-slate-400">Year {payload[0].payload.year}</div>
                          <div className="text-cyan-400 font-bold text-sm">
                            {formatExact(payload[0].value)} units
                          </div>
                        </div>
                      );
                    }
                    return null;
                  }}
                />
                <Bar dataKey="production" radius={[4, 4, 0, 0]}>
                  {yearlyChartData.map((entry, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={entry.isActive ? '#00E5FF' : entry.isPeak ? '#00E676' : '#1E293B'}
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        {/* Card 4: Budget / Commodity Distribution Donut + Horizontal Bars */}
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="glass-panel p-5"
        >
          <div className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
            Commodity Allocation // Category Share
          </div>

          <div className="grid grid-cols-1 md:grid-cols-12 gap-3 items-center">
            {/* Donut Chart with Centered KPI */}
            <div className="md:col-span-5 relative h-36 flex items-center justify-center">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={categoryData}
                    innerRadius={44}
                    outerRadius={62}
                    paddingAngle={3}
                    dataKey="value"
                  >
                    {categoryData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={CAT_COLORS[index % CAT_COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip
                    content={({ active, payload }) => {
                      if (active && payload && payload.length) {
                        return (
                          <div className="bg-slate-900 border border-cyan-500/40 p-2 rounded-lg text-xs font-mono">
                            <span className="text-slate-200 font-bold">{payload[0].name}: </span>
                            <span className="text-cyan-400">{payload[0].payload.share.toFixed(1)}%</span>
                          </div>
                        );
                      }
                      return null;
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
              <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                <span className="text-xs font-black font-mono text-cyan-400">
                  {formatLargeNumber(displayProd)}
                </span>
                <span className="text-[9px] uppercase tracking-wider text-slate-400 font-medium">TOTAL</span>
              </div>
            </div>

            {/* Split Progress Bars */}
            <div className="md:col-span-7 flex flex-col gap-2.5">
              {categoryData.slice(0, 4).map((cat, idx) => (
                <div key={cat.name} className="flex flex-col gap-1">
                  <div className="flex justify-between text-xs">
                    <span className="text-slate-300 font-medium truncate max-w-[140px]">{cat.name}</span>
                    <span className="font-mono text-cyan-400 font-bold text-[11px]">{cat.share.toFixed(1)}%</span>
                  </div>
                  <div className="w-full bg-slate-800/80 rounded-full h-1.5 overflow-hidden">
                    <div
                      className="h-full rounded-full"
                      style={{ width: `${cat.share}%`, backgroundColor: CAT_COLORS[idx % CAT_COLORS.length] }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </motion.div>

        {/* Card 5: Compare Costs / Rainfall vs Yield Area Wave Chart */}
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.25 }}
          className="glass-panel p-5"
        >
          <div className="flex justify-between items-center mb-2">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
              <Droplets size={13} className="text-cyan-400" />
              RAINFALL (MM) VS. YIELD DYNAMICS
            </span>
            <div className="text-[11px] font-mono text-slate-400 flex items-center gap-2">
              <span className="text-cyan-400">● Rain</span>
              <span className="text-emerald-400">● Yield (x10)</span>
            </div>
          </div>

          <div className="w-full h-36">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={waveData} margin={{ top: 5, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="rainGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#00E5FF" stopOpacity={0.25} />
                    <stop offset="95%" stopColor="#00E5FF" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="yieldGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#00E676" stopOpacity={0.25} />
                    <stop offset="95%" stopColor="#00E676" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <XAxis dataKey="year" stroke="#64748B" fontSize={10} tickLine={false} interval={3} />
                <YAxis stroke="#64748B" fontSize={10} tickLine={false} />
                <Tooltip
                  content={({ active, payload }) => {
                    if (active && payload && payload.length) {
                      return (
                        <div className="bg-slate-900 border border-cyan-500/40 p-2 rounded-lg text-xs font-mono">
                          <div className="text-slate-400">Year {payload[0].payload.year}</div>
                          <div className="text-cyan-400">Rainfall: {payload[0].value} mm</div>
                          <div className="text-emerald-400">Yield Idx: {payload[1].value}</div>
                        </div>
                      );
                    }
                    return null;
                  }}
                />
                <Area type="monotone" dataKey="rainfall" stroke="#00E5FF" strokeWidth={2} fillOpacity={1} fill="url(#rainGrad)" />
                <Area type="monotone" dataKey="yieldIndex" stroke="#00E676" strokeWidth={2} strokeDasharray="3 3" fillOpacity={1} fill="url(#yieldGrad)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </motion.div>
      </div>

      {/* ==================================================================== */}
      {/* RIGHT COLUMN (Cols: 4 / 12) - Cards 6, 7 & 8                         */}
      {/* ==================================================================== */}
      <div className="lg:col-span-4 flex flex-col gap-5">
        {/* Card 6: Structure / Agronomic Radar Chart */}
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="glass-panel p-5"
        >
          <div className="flex justify-between items-center mb-1">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
              <Layers size={13} className="text-cyan-400" />
              STRUCTURE // AGRONOMIC BALANCE
            </span>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/30">
              OPTIMAL
            </span>
          </div>

          <div className="w-full h-44 flex items-center justify-center">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={radarData}>
                <PolarGrid stroke="#334155" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: '#94A3B8', fontSize: 10 }} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} stroke="#334155" />
                <Radar name="Agronomic Balance" dataKey="A" stroke="#00E5FF" strokeWidth={2} fill="#00E5FF" fillOpacity={0.25} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        {/* Card 7: Costs / Regional Production Share Donut */}
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.25 }}
          className="glass-panel p-5"
        >
          <div className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
            Regional Output Share // Top States
          </div>

          <div className="grid grid-cols-1 md:grid-cols-12 gap-2 items-center">
            <div className="md:col-span-5 relative h-36 flex items-center justify-center">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={topStatesDonut}
                    innerRadius={42}
                    outerRadius={60}
                    paddingAngle={3}
                    dataKey="value"
                  >
                    {topStatesDonut.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={STATE_COLORS[index % STATE_COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip
                    content={({ active, payload }) => {
                      if (active && payload && payload.length) {
                        return (
                          <div className="bg-slate-900 border border-emerald-500/40 p-2 rounded-lg text-xs font-mono">
                            <span className="text-slate-200 font-bold">{payload[0].name}: </span>
                            <span className="text-emerald-400">{payload[0].payload.share.toFixed(1)}%</span>
                          </div>
                        );
                      }
                      return null;
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
              <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                <span className="text-xs font-black font-mono text-emerald-400">{data.kpis.states_count}</span>
                <span className="text-[9px] uppercase tracking-wider text-slate-400 font-medium">STATES</span>
              </div>
            </div>

            <div className="md:col-span-7 flex flex-col gap-2">
              {topStatesDonut.slice(0, 4).map((s, idx) => (
                <div key={s.name} className="flex justify-between items-center text-xs">
                  <span className="text-slate-300 font-medium flex items-center gap-1.5 truncate max-w-[130px]">
                    <span className="w-2 h-2 rounded-full" style={{ backgroundColor: STATE_COLORS[idx] }} />
                    {s.name}
                  </span>
                  <span className="font-mono text-emerald-400 font-bold text-[11px]">{s.share.toFixed(1)}%</span>
                </div>
              ))}
            </div>
          </div>
        </motion.div>

        {/* Card 8: Annual Plans / Multi-Year Milestone Bars */}
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="glass-panel p-5"
        >
          <div className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
            Annual Plans // Milestone Comparisons
          </div>
          <div className="w-full h-32">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={milestoneData} margin={{ top: 5, right: 10, left: -20, bottom: 0 }}>
                <XAxis dataKey="year" stroke="#64748B" fontSize={10} tickLine={false} />
                <YAxis stroke="#64748B" fontSize={10} tickLine={false} tickFormatter={formatLargeNumber} />
                <Tooltip
                  cursor={{ fill: 'rgba(0, 229, 255, 0.05)' }}
                  content={({ active, payload }) => {
                    if (active && payload && payload.length) {
                      return (
                        <div className="bg-slate-900 border border-cyan-500/40 p-2 rounded-lg text-xs font-mono">
                          <span className="text-cyan-400 font-bold">{formatLargeNumber(payload[0].value)}</span>
                        </div>
                      );
                    }
                    return null;
                  }}
                />
                <Bar dataKey="production" fill="#00E5FF" radius={[4, 4, 0, 0]}>
                  {milestoneData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={index === milestoneData.length - 1 ? '#00E676' : '#2979FF'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
