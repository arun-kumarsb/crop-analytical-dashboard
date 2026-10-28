import React, { useState, useEffect, useMemo } from 'react';
import Navbar from './components/Navbar';
import DashboardView from './components/DashboardView';
import SpatialMapView from './components/SpatialMapView';
import StateExplorerView from './components/StateExplorerView';
import CropIntelligenceView from './components/CropIntelligenceView';
import CropSimulatorView from './components/CropSimulatorView';
import CropBattleView from './components/CropBattleView';
import DataTableView from './components/DataTableView';
import agriData from './data/agri_data.json';
import { setSoundMuted } from './soundEffects';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [activeYear, setActiveYear] = useState('All');
  const [theme, setTheme] = useState('dark');
  const [selectedState, setSelectedState] = useState('Punjab');
  const [selectedCrop, setSelectedCrop] = useState('Wheat');
  const [excludeCoconut, setExcludeCoconut] = useState(false);
  const [soundMutedState, setSoundMutedState] = useState(false);

  // Sync audio mute state with Web Audio API synthesizer
  const handleSetSoundMuted = (muted) => {
    setSoundMutedState(muted);
    setSoundMuted(muted);
  };

  // Handle dynamic dataset slice (Coconut excluded vs all commodities)
  const activeData = useMemo(() => {
    if (!excludeCoconut || !agriData.no_coconut) {
      return agriData;
    }
    return {
      ...agriData,
      kpis: agriData.no_coconut.kpis,
      yearly: agriData.no_coconut.yearly,
      categories: agriData.no_coconut.categories,
      top_crops: agriData.no_coconut.top_crops,
      states: agriData.no_coconut.states,
      state_yearly: agriData.no_coconut.state_yearly,
      milestones: agriData.no_coconut.milestones,
    };
  }, [excludeCoconut]);

  // Handle theme body class updates
  useEffect(() => {
    document.documentElement.className = theme;
    if (theme === 'dark') {
      document.body.style.backgroundColor = '#070D18';
      document.body.style.color = '#F8FAFC';
    } else if (theme === 'slate') {
      document.body.style.backgroundColor = '#1E2538';
      document.body.style.color = '#F1F5F9';
    } else {
      document.body.style.backgroundColor = '#F1F5F9';
      document.body.style.color = '#0F172A';
    }
  }, [theme]);

  const handleStateDrilldown = (stateName) => {
    setSelectedState(stateName);
    setActiveTab('state');
  };

  const handleCropDrilldown = (cropName) => {
    setSelectedCrop(cropName);
    setActiveTab('crop');
  };

  return (
    <div className={`min-h-screen p-4 md:p-7 max-w-[1600px] mx-auto transition-colors duration-300 font-sans`}>
      {/* Top Navbar */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        activeYear={activeYear}
        setActiveYear={setActiveYear}
        theme={theme}
        setTheme={setTheme}
        excludeCoconut={excludeCoconut}
        setExcludeCoconut={setExcludeCoconut}
        soundMuted={soundMutedState}
        setSoundMuted={handleSetSoundMuted}
      />

      {/* Main Views */}
      <main className="w-full">
        {activeTab === 'dashboard' && (
          <DashboardView
            data={activeData}
            activeYear={activeYear}
            onSelectState={handleStateDrilldown}
            onSelectCrop={handleCropDrilldown}
            excludeCoconut={excludeCoconut}
          />
        )}

        {activeTab === 'map' && (
          <SpatialMapView
            data={activeData}
            onSelectState={handleStateDrilldown}
          />
        )}

        {activeTab === 'state' && (
          <StateExplorerView
            data={activeData}
            selectedState={selectedState}
            onSelectState={setSelectedState}
          />
        )}

        {activeTab === 'crop' && (
          <CropIntelligenceView
            data={activeData}
            selectedCrop={selectedCrop}
            onSelectCrop={setSelectedCrop}
          />
        )}

        {activeTab === 'simulator' && (
          <CropSimulatorView
            data={activeData}
            onSelectCrop={handleCropDrilldown}
          />
        )}

        {activeTab === 'battle' && (
          <CropBattleView
            data={activeData}
          />
        )}

        {activeTab === 'data' && (
          <DataTableView
            data={activeData}
          />
        )}
      </main>

      {/* Footer */}
      <footer className="mt-12 text-center text-xs font-mono text-slate-500 pb-6 border-t border-slate-800/60 pt-4 flex flex-wrap justify-between items-center gap-2">
        <span className="flex items-center gap-2">
          <span>🌾 AGRI-INTELLIGENCE // RESEARCH COMMAND CENTER</span>
          {excludeCoconut && (
            <span className="px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/30 text-[10px]">
              FILTER: TONNES ONLY (COCONUT EXCLUDED)
            </span>
          )}
        </span>
        <span>BENCHMARKS: ICAR • NBSS&LUP • DES • TNAU • OPEN-METEO WMO</span>
        <span className="text-cyan-400 flex items-center gap-1.5">
          <span className="w-2 h-2 rounded-full bg-cyan-400 animate-ping inline-block" />
          STATUS: INDUSTRY PRODUCTION LIVE 60 FPS
        </span>
      </footer>
    </div>
  );
}
