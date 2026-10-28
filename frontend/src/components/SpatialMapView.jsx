import React, { useState, useEffect, useMemo, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { geoMercator, geoPath } from 'd3-geo';
import { Play, Pause, RotateCcw, Compass, Droplets, TrendingUp, Layers, CheckCircle2 } from 'lucide-react';
import { formatLargeNumber } from '../utils';
import indiaGeoData from '../data/india_states.json';

export default function SpatialMapView({ data, onSelectState }) {
  const [metric, setMetric] = useState('production');
  const [isPlaying, setIsPlaying] = useState(false);
  const [yearIndex, setYearIndex] = useState(data.yearly.length - 2); // Default to 2019
  const [hoveredState, setHoveredState] = useState(null);
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });

  const years = useMemo(() => data.yearly.map(y => y.Crop_Year), [data.yearly]);
  const currentYear = years[yearIndex] || 2019;

  // D3 Geo Projection for India
  const { paths, stateFeatureMap } = useMemo(() => {
    const projection = geoMercator().fitSize([720, 760], indiaGeoData);
    const pathGen = geoPath().projection(projection);
    const featureMap = {};
    const pathList = indiaGeoData.features.map(f => {
      const name = f.properties.ST_NM;
      featureMap[name] = f;
      return {
        name,
        d: pathGen(f),
      };
    });
    return { paths: pathList, stateFeatureMap: featureMap };
  }, []);

  // Compute color scale for the current year & metric
  const stateYearMap = data.state_yearly[String(currentYear)] || {};
  const metricValues = Object.values(stateYearMap).map(v => v[metric] || 0);
  const maxVal = Math.max(...metricValues, 1);

  // Auto-play timer for animation
  useEffect(() => {
    let interval = null;
    if (isPlaying) {
      interval = setInterval(() => {
        setYearIndex(prev => {
          if (prev >= years.length - 1) {
            setIsPlaying(false);
            return prev;
          }
          return prev + 1;
        });
      }, 700);
    }
    return () => clearInterval(interval);
  }, [isPlaying, years.length]);

  // Color generator
  const getColor = (stateName) => {
    const val = stateYearMap[stateName]?.[metric] || 0;
    if (!val) return 'rgba(30, 41, 59, 0.6)';
    const ratio = Math.min(1, Math.max(0.12, val / maxVal));

    if (metric === 'production') {
      return `rgba(0, 229, 255, ${0.15 + ratio * 0.8})`;
    } else if (metric === 'yield') {
      return `rgba(0, 230, 118, ${0.15 + ratio * 0.8})`;
    } else if (metric === 'rainfall') {
      return `rgba(41, 121, 255, ${0.15 + ratio * 0.8})`;
    }
    return `rgba(255, 179, 0, ${0.15 + ratio * 0.8})`;
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 w-full">
      {/* Map Canvas (Left 8 cols) */}
      <div className="lg:col-span-8 glass-panel p-6 flex flex-col items-center relative overflow-hidden">
        {/* Floating Controls Bar */}
        <div className="w-full flex flex-wrap items-center justify-between gap-4 mb-4 z-10">
          <div>
            <div className="text-xs font-bold uppercase tracking-wider text-cyan-400 font-mono flex items-center gap-1.5">
              <Compass size={14} /> SPATIAL CARTOGRAPHY // INDIA
            </div>
            <div className="text-sm font-extrabold text-white">Interactive State Boundaries & Heatmap</div>
          </div>

          {/* Metric Selector Pills */}
          <div className="flex items-center gap-1.5 bg-slate-900/80 p-1.5 rounded-xl border border-slate-700/60 text-xs font-mono">
            {[
              { id: 'production', label: '🌾 Production' },
              { id: 'yield', label: '📈 Mean Yield' },
              { id: 'rainfall', label: '🌧️ Rainfall' },
            ].map(m => (
              <button
                key={m.id}
                onClick={() => setMetric(m.id)}
                className={`px-3 py-1.5 rounded-lg transition-all ${
                  metric === m.id
                    ? 'bg-cyan-500 text-slate-950 font-bold shadow-md shadow-cyan-500/20'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                {m.label}
              </button>
            ))}
          </div>
        </div>

        {/* SVG Map Container */}
        <div
          className="relative w-full max-w-[700px] aspect-[1/1.05] flex items-center justify-center cursor-crosshair"
          onMouseMove={e => {
            const rect = e.currentTarget.getBoundingClientRect();
            setMousePos({ x: e.clientX - rect.left, y: e.clientY - rect.top });
          }}
          onMouseLeave={() => setHoveredState(null)}
        >
          <svg viewBox="0 0 720 760" className="w-full h-full filter drop-shadow-[0_10px_25px_rgba(0,0,0,0.6)]">
            {paths.map(({ name, d }) => {
              const isHovered = hoveredState === name;
              const fill = getColor(name);
              return (
                <path
                  key={name}
                  d={d}
                  fill={fill}
                  stroke={isHovered ? '#00E5FF' : 'rgba(0, 229, 255, 0.35)'}
                  strokeWidth={isHovered ? 2.5 : 1}
                  className="transition-colors duration-300 hover:brightness-125"
                  onMouseEnter={() => setHoveredState(name)}
                  onClick={() => onSelectState && onSelectState(name)}
                />
              );
            })}
          </svg>

          {/* Dynamic Floating Tooltip */}
          {hoveredState && (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              style={{ left: Math.min(480, mousePos.x + 15), top: Math.max(10, mousePos.y - 70) }}
              className="absolute pointer-events-none z-30 bg-slate-950/90 backdrop-blur-md border border-cyan-400/50 p-3.5 rounded-xl shadow-2xl text-xs font-mono min-w-[200px]"
            >
              <div className="font-extrabold text-cyan-400 text-sm mb-1">{hoveredState}</div>
              <div className="text-slate-400 text-[11px] mb-2">Harvest Year: {currentYear}</div>
              <div className="space-y-1">
                <div className="flex justify-between">
                  <span className="text-slate-400">Production:</span>
                  <span className="text-white font-bold">{formatLargeNumber(stateYearMap[hoveredState]?.production || 0)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Mean Yield:</span>
                  <span className="text-emerald-400 font-bold">{(stateYearMap[hoveredState]?.yield || 0).toFixed(2)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Rainfall:</span>
                  <span className="text-blue-400 font-bold">{Math.round(stateYearMap[hoveredState]?.rainfall || 0)} mm</span>
                </div>
              </div>
              <div className="mt-2 pt-2 border-t border-slate-800 text-[10px] text-cyan-300/80 text-center">
                👉 Click to inspect state profile
              </div>
            </motion.div>
          )}
        </div>

        {/* Timeline Scrubber & Animation Controls */}
        <div className="w-full bg-slate-900/80 border border-slate-700/50 rounded-2xl p-4 mt-4 flex items-center gap-4 z-10">
          <button
            onClick={() => setIsPlaying(!isPlaying)}
            className="w-10 h-10 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-black flex items-center justify-center transition-all shadow-lg shadow-cyan-500/20"
          >
            {isPlaying ? <Pause size={18} /> : <Play size={18} className="ml-0.5" />}
          </button>

          <button
            onClick={() => { setIsPlaying(false); setYearIndex(0); }}
            className="p-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 transition-all"
            title="Reset to 1997"
          >
            <RotateCcw size={16} />
          </button>

          {/* Scrubber Slider */}
          <div className="flex-1 flex flex-col gap-1">
            <div className="flex justify-between text-xs font-mono">
              <span className="text-slate-400">1997</span>
              <span className="text-cyan-400 font-extrabold text-sm tracking-wider">
                ACTIVE YEAR: {currentYear}
              </span>
              <span className="text-slate-400">2020</span>
            </div>
            <input
              type="range"
              min={0}
              max={years.length - 1}
              value={yearIndex}
              onChange={e => { setIsPlaying(false); setYearIndex(Number(e.target.value)); }}
              className="w-full h-1.5 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-cyan-400"
            />
          </div>
        </div>
      </div>

      {/* State Quick-Insights Sidebar (Right 4 cols) */}
      <div className="lg:col-span-4 flex flex-col gap-5">
        <div className="glass-panel p-5">
          <div className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-1">
            Spatial Summary // {currentYear}
          </div>
          <div className="text-base font-extrabold text-white mb-4">
            State Rankings in {currentYear}
          </div>

          {/* Top States List for active year */}
          <div className="flex flex-col gap-2.5">
            {Object.entries(stateYearMap)
              .sort((a, b) => (b[1][metric] || 0) - (a[1][metric] || 0))
              .slice(0, 7)
              .map(([stName, stVals], idx) => {
                const val = stVals[metric] || 0;
                const pct = Math.min(100, (val / maxVal) * 100);
                return (
                  <div
                    key={stName}
                    onClick={() => onSelectState && onSelectState(stName)}
                    className="p-2.5 rounded-xl bg-slate-900/60 hover:bg-cyan-500/10 border border-slate-800 hover:border-cyan-500/40 cursor-pointer transition-all flex flex-col gap-1.5"
                  >
                    <div className="flex justify-between items-center text-xs">
                      <span className="font-semibold text-slate-200 flex items-center gap-2">
                        <span className="w-5 h-5 rounded-full bg-slate-800 text-[10px] font-mono flex items-center justify-center font-bold text-cyan-400">
                          {idx + 1}
                        </span>
                        {stName}
                      </span>
                      <span className="font-mono text-cyan-400 font-bold text-xs">
                        {metric === 'yield' ? val.toFixed(2) : formatLargeNumber(val)}
                      </span>
                    </div>
                    <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                      <div className="h-full bg-gradient-to-r from-blue-500 to-cyan-400 rounded-full" style={{ width: `${pct}%` }} />
                    </div>
                  </div>
                );
              })}
          </div>
        </div>

        {/* Agronomic Analytical Box */}
        <div className="glass-panel p-5 bg-gradient-to-br from-slate-900 via-slate-900 to-cyan-950/30 border border-cyan-500/20">
          <div className="text-xs font-bold uppercase text-cyan-400 font-mono mb-2 flex items-center gap-1.5">
            <CheckCircle2 size={14} /> AUTONOMOUS OBSERVATION
          </div>
          <p className="text-xs text-slate-300 leading-relaxed">
            In {currentYear}, agricultural output concentrated heavily in alluvial river basins and coastal deltas.
            Notice how Punjab, Haryana, and Uttar Pradesh sustain peak grain yields through extensive irrigation,
            independent of monsoonal rainfall deficits.
          </p>
        </div>
      </div>
    </div>
  );
}
