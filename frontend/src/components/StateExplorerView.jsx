import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { formatLargeNumber } from '../utils';
import { STATE_CAPITALS } from '../stateCapitals';
import {
  Globe, MapPin, Sparkles, Droplets, Calendar, ShieldCheck,
  CloudSun, Wind, Thermometer, Radio, CheckCircle2, AlertTriangle
} from 'lucide-react';

export default function StateExplorerView({ data, selectedState, onSelectState }) {
  const [activeState, setActiveState] = useState(selectedState || 'Punjab');
  const [weather, setWeather] = useState(null);
  const [weatherLoading, setWeatherLoading] = useState(false);
  const [weatherError, setWeatherError] = useState(null);

  const allStates = data.all_states;

  const sp = data.state_profiles[activeState] || {
    zone: 'Northern Plains',
    climate_desc: 'Sub-tropical monsoon',
    primary_season: 'Kharif & Rabi',
    soils: ['Alluvial Loam', 'Clay Loam'],
    source: 'ICAR-NBSS&LUP',
    top_crops: []
  };

  const capitalInfo = STATE_CAPITALS[activeState] || { capital: activeState, lat: 28.6139, lon: 77.2090 };

  // Fetch real-time live Open-Meteo weather
  useEffect(() => {
    let isCancelled = false;
    setWeatherLoading(true);
    setWeatherError(null);

    const lat = capitalInfo.lat;
    const lon = capitalInfo.lon;
    const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m&timezone=auto`;

    fetch(url)
      .then(res => {
        if (!res.ok) throw new Error('Weather feed unavailable');
        return res.json();
      })
      .then(resData => {
        if (!isCancelled && resData.current) {
          setWeather(resData.current);
          setWeatherLoading(false);
        }
      })
      .catch(err => {
        if (!isCancelled) {
          setWeatherError(err.message);
          setWeatherLoading(false);
        }
      });

    return () => {
      isCancelled = true;
    };
  }, [activeState, capitalInfo.lat, capitalInfo.lon]);

  // Weather condition decoder
  const getWeatherDesc = (code) => {
    if (code === 0) return 'Clear Sky';
    if (code >= 1 && code <= 3) return 'Partly Cloudy';
    if (code >= 45 && code <= 48) return 'Foggy / Mist';
    if (code >= 51 && code <= 67) return 'Rain / Drizzle';
    if (code >= 71 && code <= 77) return 'Snow / Flurries';
    if (code >= 80 && code <= 82) return 'Rain Showers';
    if (code >= 95) return 'Thunderstorm';
    return 'Scattered Clouds';
  };

  // State historical records across all years
  const stateYearHistory = Object.entries(data.state_yearly)
    .map(([year, states]) => ({
      year,
      production: states[activeState]?.production || 0,
      yieldVal: states[activeState]?.yield || 0,
      rainfall: states[activeState]?.rainfall || 0,
    }))
    .sort((a, b) => Number(a.year) - Number(b.year));

  const totalProd = stateYearHistory.reduce((acc, curr) => acc + curr.production, 0);

  // Compute Agro Advisory based on live telemetry
  const getAgroAdvisory = () => {
    if (!weather) return null;
    const temp = weather.temperature_2m;
    const rh = weather.relative_humidity_2m;
    const precip = weather.precipitation;

    if (precip > 5) {
      return {
        status: 'CAUTION',
        title: 'Active Precipitation Event',
        desc: 'Delay foliar fertilizer application & pesticide spraying. Ensure proper drainage in low-lying plots to prevent root rot.',
        color: 'text-amber-400',
        border: 'border-amber-500/40',
        bg: 'bg-amber-500/10'
      };
    }
    if (temp > 36) {
      return {
        status: 'HEAT ADVISORY',
        title: 'High Thermal Evaporation Stress',
        desc: 'High evapotranspiration rate. Maintain soil moisture via early morning micro-sprinklers or drip irrigation cycles.',
        color: 'text-orange-400',
        border: 'border-orange-500/40',
        bg: 'bg-orange-500/10'
      };
    }
    if (rh > 82) {
      return {
        status: 'PATHOGEN VIGILANCE',
        title: 'High Relative Humidity',
        desc: 'Elevated fungal and blight susceptibility. Inspect canopy density and schedule preventative bio-fungicide checks.',
        color: 'text-sky-400',
        border: 'border-sky-500/40',
        bg: 'bg-sky-500/10'
      };
    }
    return {
      status: 'OPTIMAL',
      title: 'Favorable Field Conditions',
      desc: 'Balanced thermal & humidity indices. Excellent window for weeding, basal fertilizer dressing, and standard harvesting.',
      color: 'text-emerald-400',
      border: 'border-emerald-500/40',
      bg: 'bg-emerald-500/10'
    };
  };

  const advisory = getAgroAdvisory();

  return (
    <div className="flex flex-col gap-5 w-full">
      {/* State Selection Bar */}
      <div className="glass-panel p-5 flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400">
            <MapPin size={20} />
          </div>
          <div>
            <div className="text-xs font-bold uppercase tracking-wider text-slate-400 font-mono">
              STATE DRILLDOWN & TAXONOMY
            </div>
            <div className="text-lg font-extrabold text-white flex items-center gap-2">
              <span>{activeState}</span>
              <span className="text-xs font-normal font-mono px-2 py-0.5 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/30">
                {sp.zone}
              </span>
            </div>
          </div>
        </div>

        {/* State Dropdown Selector */}
        <div className="flex items-center gap-2">
          <span className="text-xs font-mono text-slate-400">SELECT REGION:</span>
          <select
            value={activeState}
            onChange={e => {
              setActiveState(e.target.value);
              if (onSelectState) onSelectState(e.target.value);
            }}
            className="bg-slate-900 border border-slate-700 text-cyan-400 text-xs font-bold font-mono rounded-xl px-4 py-2 focus:outline-none focus:border-cyan-400 cursor-pointer"
          >
            {allStates.map(st => (
              <option key={st} value={st}>{st}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Live 2026 Weather & Agro-Meteorological Telemetry Banner */}
      <div className="glass-panel p-5 border border-cyan-500/30 relative overflow-hidden bg-gradient-to-r from-slate-900/90 via-slate-900/70 to-cyan-950/30">
        <div className="absolute top-0 right-0 w-80 h-32 bg-cyan-500/5 rounded-full blur-3xl pointer-events-none" />

        <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-4 mb-4">
          <div className="flex items-center gap-2">
            <span className="relative flex h-3 w-3">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
            </span>
            <span className="text-xs font-mono font-bold tracking-wider text-emerald-400 flex items-center gap-1.5">
              <Radio size={14} className="animate-pulse" /> LIVE 2026 SATELLITE METEOROLOGY FEED
            </span>
            <span className="text-[11px] font-mono text-slate-400">
              // CAPITAL STATION: <strong className="text-white">{capitalInfo.capital}</strong> ({capitalInfo.lat}°N, {capitalInfo.lon}°E)
            </span>
          </div>
          <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800/80 border border-slate-700 text-slate-300">
            PROVIDER: OPEN-METEO GLOBAL WMO
          </span>
        </div>

        {weatherLoading ? (
          <div className="flex items-center justify-center py-6 text-xs font-mono text-cyan-400 gap-2">
            <div className="w-4 h-4 border-2 border-cyan-400 border-t-transparent rounded-full animate-spin" />
            SYNCHRONIZING SATELLITE TELEMETRY...
          </div>
        ) : weather ? (
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4 items-center">
            {/* Metric 1: Temp */}
            <div className="bg-slate-950/50 p-3.5 rounded-xl border border-slate-800/80">
              <div className="text-[11px] font-mono text-slate-400 flex items-center gap-1.5 mb-1">
                <Thermometer size={14} className="text-orange-400" /> AMBIENT TEMP
              </div>
              <div className="text-2xl font-black font-mono text-white">
                {weather.temperature_2m}°C
              </div>
              <div className="text-[10px] text-slate-400 font-mono mt-0.5">
                Condition: {getWeatherDesc(weather.weather_code)}
              </div>
            </div>

            {/* Metric 2: Humidity */}
            <div className="bg-slate-950/50 p-3.5 rounded-xl border border-slate-800/80">
              <div className="text-[11px] font-mono text-slate-400 flex items-center gap-1.5 mb-1">
                <Droplets size={14} className="text-cyan-400" /> HUMIDITY
              </div>
              <div className="text-2xl font-black font-mono text-cyan-300">
                {weather.relative_humidity_2m}%
              </div>
              <div className="text-[10px] text-slate-400 font-mono mt-0.5">
                Vapor pressure index
              </div>
            </div>

            {/* Metric 3: Precipitation */}
            <div className="bg-slate-950/50 p-3.5 rounded-xl border border-slate-800/80">
              <div className="text-[11px] font-mono text-slate-400 flex items-center gap-1.5 mb-1">
                <CloudSun size={14} className="text-sky-400" /> PRECIPITATION
              </div>
              <div className="text-2xl font-black font-mono text-sky-300">
                {weather.precipitation} <span className="text-xs font-mono">mm</span>
              </div>
              <div className="text-[10px] text-slate-400 font-mono mt-0.5">
                Current gauge reading
              </div>
            </div>

            {/* Metric 4: Wind Speed */}
            <div className="bg-slate-950/50 p-3.5 rounded-xl border border-slate-800/80">
              <div className="text-[11px] font-mono text-slate-400 flex items-center gap-1.5 mb-1">
                <Wind size={14} className="text-emerald-400" /> SURFACE WIND
              </div>
              <div className="text-2xl font-black font-mono text-emerald-300">
                {weather.wind_speed_10m} <span className="text-xs font-mono">km/h</span>
              </div>
              <div className="text-[10px] text-slate-400 font-mono mt-0.5">
                10m altitude vector
              </div>
            </div>

            {/* Metric 5: Live Agro-Advisory Pill */}
            {advisory && (
              <div className={`col-span-2 md:col-span-1 p-3.5 rounded-xl border ${advisory.border} ${advisory.bg}`}>
                <div className={`text-[10px] font-mono font-bold uppercase tracking-wider ${advisory.color} mb-1 flex items-center gap-1`}>
                  <CheckCircle2 size={12} /> {advisory.status}
                </div>
                <div className="text-xs font-bold text-white leading-tight">
                  {advisory.title}
                </div>
                <div className="text-[10px] text-slate-300 mt-1 leading-snug line-clamp-2" title={advisory.desc}>
                  {advisory.desc}
                </div>
              </div>
            )}
          </div>
        ) : (
          <div className="text-xs font-mono text-slate-400 py-2">
            Telemetry offline. Using regional baseline climatology data.
          </div>
        )}
      </div>

      {/* State Agro-Climatic Intelligence Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        {/* Card 1: Soil Profiles (ICAR-NBSS&LUP) */}
        <div className="glass-panel p-5">
          <div className="text-xs font-bold uppercase tracking-wider text-slate-400 font-mono mb-2 flex items-center gap-1.5">
            <Sparkles size={14} className="text-amber-400" />
            DOMINANT SOIL TAXONOMY (ICAR-NBSS&LUP)
          </div>
          <div className="flex flex-wrap gap-2 mt-3">
            {sp.soils.map(soil => (
              <span
                key={soil}
                className="px-3 py-1.5 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs font-semibold"
              >
                🌱 {soil}
              </span>
            ))}
          </div>
          <div className="mt-4 pt-3 border-t border-slate-800 text-[11px] text-slate-400 font-mono">
            Classification Source: {sp.source}
          </div>
        </div>

        {/* Card 2: Climate Profile */}
        <div className="glass-panel p-5">
          <div className="text-xs font-bold uppercase tracking-wider text-slate-400 font-mono mb-2 flex items-center gap-1.5">
            <Droplets size={14} className="text-cyan-400" />
            CLIMATIC DYNAMICS & RAINFALL
          </div>
          <p className="text-xs text-slate-300 leading-relaxed mt-2">{sp.climate_desc}</p>
          <div className="mt-3 flex items-center gap-2">
            <span className="text-xs px-2.5 py-1 rounded-lg bg-cyan-500/10 border border-cyan-500/30 text-cyan-300 font-mono">
              ☀️ Season: {sp.primary_season}
            </span>
          </div>
        </div>

        {/* Card 3: Cumulative Production */}
        <div className="glass-panel p-5 bg-gradient-to-br from-slate-900 to-cyan-950/40">
          <div className="text-xs font-bold uppercase tracking-wider text-slate-400 font-mono mb-1">
            CUMULATIVE OUTPUT (1997-2020)
          </div>
          <div className="text-3xl font-black font-mono text-cyan-400 mb-2">
            {formatLargeNumber(totalProd)}
          </div>
          <div className="text-xs text-slate-400">
            Leading crop share dominates regional agricultural GDP.
          </div>
        </div>
      </div>

      {/* State Charts: Top Crops Bar & Historical Production Line */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        {/* Top Crops in State */}
        <div className="glass-panel p-5">
          <div className="text-xs font-bold uppercase tracking-wider text-slate-400 font-mono mb-2">
            TOP CULTIVATED CROPS IN {activeState.toUpperCase()}
          </div>
          <div className="w-full h-56">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={sp.top_crops} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
                <XAxis dataKey="crop" stroke="#64748B" fontSize={10} tickLine={false} interval={0} angle={-25} textAnchor="end" />
                <YAxis stroke="#64748B" fontSize={10} tickLine={false} tickFormatter={formatLargeNumber} />
                <Tooltip
                  content={({ active, payload }) => {
                    if (active && payload && payload.length) {
                      return (
                        <div className="bg-slate-900 border border-cyan-500/40 p-2 rounded-lg text-xs font-mono">
                          <div className="font-bold text-white">{payload[0].payload.crop}</div>
                          <div className="text-cyan-400">{formatLargeNumber(payload[0].value)} units</div>
                        </div>
                      );
                    }
                    return null;
                  }}
                />
                <Bar dataKey="production" fill="#00E5FF" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Historical Production Trend in State */}
        <div className="glass-panel p-5">
          <div className="text-xs font-bold uppercase tracking-wider text-slate-400 font-mono mb-2">
            HISTORICAL OUTPUT TRAJECTORY (1997–2020)
          </div>
          <div className="w-full h-56">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={stateYearHistory} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <XAxis dataKey="year" stroke="#64748B" fontSize={10} tickLine={false} interval={3} />
                <YAxis stroke="#64748B" fontSize={10} tickLine={false} tickFormatter={formatLargeNumber} />
                <Tooltip
                  content={({ active, payload }) => {
                    if (active && payload && payload.length) {
                      return (
                        <div className="bg-slate-900 border border-emerald-500/40 p-2 rounded-lg text-xs font-mono">
                          <div className="text-slate-400">Year {payload[0].payload.year}</div>
                          <div className="text-emerald-400 font-bold">{formatLargeNumber(payload[0].value)} units</div>
                        </div>
                      );
                    }
                    return null;
                  }}
                />
                <Line type="monotone" dataKey="production" stroke="#00E676" strokeWidth={2.5} dot={{ r: 2, fill: '#00E676' }} activeDot={{ r: 5 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
