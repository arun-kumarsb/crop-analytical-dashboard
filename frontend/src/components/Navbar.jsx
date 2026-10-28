import React from 'react';
import { motion } from 'framer-motion';
import {
  Sprout, Map, BarChart3, Globe, Database, Moon, Sun, CloudRain,
  Cpu, Swords, Volume2, VolumeX, Filter
} from 'lucide-react';
import { playClickSound, playSwitchSound } from '../soundEffects';

export default function Navbar({
  activeTab,
  setActiveTab,
  activeYear,
  setActiveYear,
  theme,
  setTheme,
  excludeCoconut,
  setExcludeCoconut,
  soundMuted,
  setSoundMuted
}) {
  const tabs = [
    { id: 'dashboard', label: 'Dashboard', icon: BarChart3 },
    { id: 'map', label: 'Spatial Map', icon: Map },
    { id: 'state', label: 'State Explorer', icon: Globe },
    { id: 'crop', label: 'Crop Intelligence', icon: Sprout },
    { id: 'simulator', label: 'Feasibility Simulator', icon: Cpu },
    { id: 'battle', label: 'Crop Battle', icon: Swords },
    { id: 'data', label: 'Records & Export', icon: Database },
  ];

  const years = ['All', '2019', '2018', '2017', '2016', '2015'];

  const handleTabClick = (tabId) => {
    playClickSound();
    setActiveTab(tabId);
  };

  const handleYearClick = (year) => {
    playClickSound();
    setActiveYear(year);
  };

  const handleCoconutToggle = () => {
    playSwitchSound();
    setExcludeCoconut(!excludeCoconut);
  };

  const handleMuteToggle = () => {
    playSwitchSound();
    setSoundMuted(!soundMuted);
  };

  return (
    <header className="w-full mb-6 z-50">
      <div className="glass-panel px-5 py-3.5 flex flex-wrap items-center justify-between gap-4">
        {/* Brand / Logo */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-400 to-emerald-500 flex items-center justify-center shadow-lg shadow-cyan-500/20 text-slate-950 font-black text-xl">
            🌾
          </div>
          <div>
            <div className="font-extrabold tracking-wider text-base flex items-center gap-1.5">
              <span>AGRI-INTELLIGENCE</span>
              <span className="text-cyan-400 font-mono">//</span>
              <span className="text-emerald-400 font-mono text-xs px-2 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/30">
                INDIA
              </span>
            </div>
            <div className="text-[11px] text-slate-400 font-medium">Industry-Grade Agronomic Intelligence</div>
          </div>
        </div>

        {/* Central Navigation Pills */}
        <nav className="flex items-center flex-wrap gap-1 bg-slate-900/70 p-1.5 rounded-2xl border border-slate-700/40">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => handleTabClick(tab.id)}
                className={`relative px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5 cursor-pointer ${
                  isActive
                    ? 'text-cyan-400'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
                }`}
              >
                {isActive && (
                  <motion.div
                    layoutId="activeTabPill"
                    className="absolute inset-0 bg-gradient-to-r from-cyan-500/20 to-emerald-500/20 border border-cyan-400/40 rounded-xl shadow-lg shadow-cyan-500/10"
                    transition={{ type: 'spring', stiffness: 350, damping: 30 }}
                  />
                )}
                <Icon size={14} className={isActive ? 'text-cyan-400' : 'text-slate-400'} />
                <span className="relative z-10">{tab.label}</span>
              </button>
            );
          })}
        </nav>

        {/* Right Controls: Coconut Toggle, Sound, Year, Theme Switcher */}
        <div className="flex items-center flex-wrap gap-2.5">
          {/* 1-Click Coconut Filter Toggle */}
          <button
            onClick={handleCoconutToggle}
            title={excludeCoconut ? "Metric Tonnes Only: Coconut Excluded" : "All Commodities (Including Nuts)"}
            className={`px-3 py-1.5 rounded-xl text-xs font-mono font-bold flex items-center gap-1.5 border transition-all cursor-pointer ${
              excludeCoconut
                ? 'bg-amber-500/20 border-amber-500/50 text-amber-300 shadow-sm shadow-amber-500/20'
                : 'bg-slate-900/60 border-slate-700/50 text-slate-400 hover:text-slate-200'
            }`}
          >
            <Filter size={13} className={excludeCoconut ? 'text-amber-400' : 'text-slate-400'} />
            <span>{excludeCoconut ? '🥥 Excl. Coconut (Tonnes Only)' : '🥥 All Commodities'}</span>
          </button>

          {/* Sound Mute/Unmute */}
          <button
            onClick={handleMuteToggle}
            title={soundMuted ? "Unmute Synthesizer Audio" : "Mute Synthesizer Audio"}
            className={`p-2 rounded-xl border transition-all cursor-pointer ${
              soundMuted
                ? 'bg-slate-900/60 border-slate-700/50 text-slate-500'
                : 'bg-cyan-500/10 border-cyan-500/40 text-cyan-400'
            }`}
          >
            {soundMuted ? <VolumeX size={15} /> : <Volume2 size={15} />}
          </button>

          {/* Year Pills */}
          <div className="flex items-center gap-1 bg-slate-900/60 p-1 rounded-xl border border-slate-700/40 text-xs font-mono">
            {years.map((y) => (
              <button
                key={y}
                onClick={() => handleYearClick(y)}
                className={`px-2.5 py-1 rounded-lg transition-all cursor-pointer ${
                  activeYear === y
                    ? 'bg-cyan-500 text-slate-950 font-bold shadow-md shadow-cyan-500/25'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                {y}
              </button>
            ))}
          </div>

          {/* Theme Toggle */}
          <div className="flex items-center gap-1 bg-slate-900/60 p-1 rounded-xl border border-slate-700/40">
            <button
              onClick={() => { playClickSound(); setTheme('dark'); }}
              title="Cyberpunk Dark"
              className={`p-1.5 rounded-lg transition-all cursor-pointer ${
                theme === 'dark' ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/40' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <Moon size={14} />
            </button>
            <button
              onClick={() => { playClickSound(); setTheme('slate'); }}
              title="Slate Neumorphic"
              className={`p-1.5 rounded-lg transition-all cursor-pointer ${
                theme === 'slate' ? 'bg-sky-500/20 text-sky-400 border border-sky-500/40' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <CloudRain size={14} />
            </button>
            <button
              onClick={() => { playClickSound(); setTheme('light'); }}
              title="Clean Light"
              className={`p-1.5 rounded-lg transition-all cursor-pointer ${
                theme === 'light' ? 'bg-amber-500/20 text-amber-400 border border-amber-500/40' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <Sun size={14} />
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}
