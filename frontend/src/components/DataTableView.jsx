import React, { useState, useMemo } from 'react';
import { Download, Search, Database, ArrowUpDown } from 'lucide-react';
import { formatLargeNumber, formatExact } from '../utils';

export default function DataTableView({ data }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCrop, setSelectedCrop] = useState('All');
  const [selectedState, setSelectedState] = useState('All');
  const [page, setPage] = useState(1);
  const rowsPerPage = 12;

  // Build searchable items from top crops & states combinations
  const rawRecords = useMemo(() => {
    const list = [];
    data.states.forEach(s => {
      data.top_crops.slice(0, 10).forEach(c => {
        list.push({
          state: s.State,
          crop: c.Crop,
          category: c.category,
          production: Math.round(s.production * (c.share_pct / 100)),
          area: Math.round(s.area * (c.share_pct / 100)),
          yieldAvg: c.yield_avg,
          rainfall: s.rainfall_avg,
        });
      });
    });
    return list;
  }, [data]);

  // Filtering
  const filtered = useMemo(() => {
    return rawRecords.filter(r => {
      const matchSearch =
        r.state.toLowerCase().includes(searchTerm.toLowerCase()) ||
        r.crop.toLowerCase().includes(searchTerm.toLowerCase()) ||
        r.category.toLowerCase().includes(searchTerm.toLowerCase());
      const matchCrop = selectedCrop === 'All' || r.crop === selectedCrop;
      const matchState = selectedState === 'All' || r.state === selectedState;
      return matchSearch && matchCrop && matchState;
    });
  }, [rawRecords, searchTerm, selectedCrop, selectedState]);

  const totalPages = Math.ceil(filtered.length / rowsPerPage);
  const paginated = filtered.slice((page - 1) * rowsPerPage, page * rowsPerPage);

  const downloadCSV = () => {
    const header = 'State,Crop,Category,Production,Area,Yield,Annual_Rainfall\n';
    const rows = filtered.map(r =>
      `"${r.state}","${r.crop}","${r.category}",${r.production},${r.area},${r.yieldAvg.toFixed(2)},${r.rainfall.toFixed(1)}`
    ).join('\n');
    const blob = new Blob([header + rows], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.setAttribute('href', url);
    link.setAttribute('download', 'agri_intelligence_records.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="flex flex-col gap-5 w-full">
      <div className="glass-panel p-5 flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400">
            <Database size={20} />
          </div>
          <div>
            <div className="text-xs font-bold uppercase tracking-wider text-slate-400 font-mono">
              RECORD INSPECTOR & EXPORT
            </div>
            <div className="text-base font-extrabold text-white">
              Aggregated Agricultural Data Records
            </div>
          </div>
        </div>

        {/* Filter Controls & CSV Download */}
        <div className="flex flex-wrap items-center gap-3">
          <div className="relative">
            <Search size={14} className="absolute left-3 top-2.5 text-slate-400" />
            <input
              type="text"
              placeholder="Search records..."
              value={searchTerm}
              onChange={e => { setSearchTerm(e.target.value); setPage(1); }}
              className="bg-slate-900 border border-slate-700 text-xs font-mono rounded-xl pl-8 pr-3 py-2 text-white focus:outline-none focus:border-cyan-400 w-44"
            />
          </div>

          <button
            onClick={downloadCSV}
            className="px-4 py-2 rounded-xl bg-gradient-to-r from-cyan-500 to-emerald-500 hover:from-cyan-400 hover:to-emerald-400 text-slate-950 font-bold text-xs flex items-center gap-2 shadow-lg shadow-cyan-500/20 transition-all"
          >
            <Download size={14} />
            <span>Export CSV</span>
          </button>
        </div>
      </div>

      {/* Table Component */}
      <div className="glass-panel p-5 overflow-x-auto">
        <table className="w-full text-left text-xs font-mono">
          <thead>
            <tr className="border-b border-slate-700 text-slate-400 uppercase text-[10px] tracking-wider">
              <th className="pb-3 px-3">State / Region</th>
              <th className="pb-3 px-3">Crop Variety</th>
              <th className="pb-3 px-3">Category</th>
              <th className="pb-3 px-3 text-right">Production</th>
              <th className="pb-3 px-3 text-right">Area (Acreage)</th>
              <th className="pb-3 px-3 text-right">Yield Index</th>
              <th className="pb-3 px-3 text-right">Rainfall (mm)</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {paginated.map((r, idx) => (
              <tr key={idx} className="hover:bg-cyan-500/5 transition-colors">
                <td className="py-2.5 px-3 font-semibold text-white">{r.state}</td>
                <td className="py-2.5 px-3 text-cyan-400 font-bold">{r.crop}</td>
                <td className="py-2.5 px-3 text-slate-400">{r.category}</td>
                <td className="py-2.5 px-3 text-right text-white font-bold">{formatExact(r.production)}</td>
                <td className="py-2.5 px-3 text-right text-slate-300">{formatExact(r.area)}</td>
                <td className="py-2.5 px-3 text-right text-emerald-400 font-bold">{r.yieldAvg.toFixed(2)}</td>
                <td className="py-2.5 px-3 text-right text-blue-400">{r.rainfall.toFixed(1)}</td>
              </tr>
            ))}
          </tbody>
        </table>

        {/* Pagination Bar */}
        <div className="flex justify-between items-center mt-4 pt-3 border-t border-slate-800 text-xs font-mono text-slate-400">
          <div>
            Showing {(page - 1) * rowsPerPage + 1}–{Math.min(page * rowsPerPage, filtered.length)} of {filtered.length} records
          </div>
          <div className="flex items-center gap-2">
            <button
              disabled={page <= 1}
              onClick={() => setPage(p => Math.max(1, p - 1))}
              className="px-3 py-1 rounded-lg bg-slate-800 disabled:opacity-30 hover:bg-slate-700 text-white"
            >
              Prev
            </button>
            <span className="text-cyan-400 font-bold">Page {page} of {totalPages || 1}</span>
            <button
              disabled={page >= totalPages}
              onClick={() => setPage(p => Math.min(totalPages, p + 1))}
              className="px-3 py-1 rounded-lg bg-slate-800 disabled:opacity-30 hover:bg-slate-700 text-white"
            >
              Next
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
