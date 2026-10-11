'use client';

import React, { useState, useEffect } from 'react';
import Navbar from '@/components/Navbar';
import CostBreakdownChart from '@/components/CostBreakdownChart';
import { 
  Calculator, 
  Printer, 
  RefreshCw 
} from 'lucide-react';
import { CostEstimate } from '@/lib/types';
import { calculateCostEstimateApi, compareEstimateTiersApi } from '@/lib/api';

export default function CostEstimationPage() {
  const [builtUpArea, setBuiltUpArea] = useState(1800);
  const [floors, setFloors] = useState(2);
  const [wallType, setWallType] = useState('AAC Lightweight Blocks');
  const [quality, setQuality] = useState('Standard Premium');
  const [estimate, setEstimate] = useState<CostEstimate | null>(null);
  const [comparisons, setComparisons] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    loadEstimate();
  }, []);

  const loadEstimate = async () => {
    setIsLoading(true);
    try {
      const res = await calculateCostEstimateApi({
        built_up_area: builtUpArea,
        floors: floors,
        wall_type: wallType,
        construction_quality: quality
      });
      setEstimate(res);

      const compRes = await compareEstimateTiersApi(builtUpArea, floors);
      setComparisons(compRes.comparisons || []);
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col">
      <Navbar />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 w-full flex-1 space-y-6">
        
        {/* Page Header */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-4 border-b border-slate-200">
          <div>
            <h1 className="text-2xl font-black text-slate-900 flex items-center gap-2.5">
              <span className="p-2 rounded-xl bg-blue-50 border border-blue-200 text-blue-600 shadow-2xs">
                <Calculator className="w-5 h-5" />
              </span>
              Construction Cost Estimation &amp; Bill of Quantities (BOQ)
            </h1>
            <p className="text-xs text-slate-600 mt-1">
              Deterministic IS 456 / IS 1200 quantity takeoff with regional price benchmarks and contingency reserves.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handlePrint}
              className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-white hover:bg-slate-50 border border-slate-300 text-slate-700 text-xs font-semibold shadow-2xs transition"
            >
              <Printer className="w-3.5 h-3.5 text-blue-600" />
              Print / Save PDF
            </button>
          </div>
        </div>

        {/* Input Controls Bar */}
        <div className="bg-white border border-slate-200 shadow-sm p-5 rounded-2xl grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div>
            <label className="text-xs font-semibold text-slate-700 block mb-1">
              Total Built-up Area (sq.ft)
            </label>
            <input
              type="number"
              value={builtUpArea}
              onChange={(e) => setBuiltUpArea(Number(e.target.value))}
              min="500"
              max="10000"
              className="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-xs text-slate-900 focus:bg-white focus:outline-none focus:border-blue-600 font-mono shadow-2xs"
            />
          </div>

          <div>
            <label className="text-xs font-semibold text-slate-700 block mb-1">
              Number of Floors
            </label>
            <select
              value={floors}
              onChange={(e) => setFloors(Number(e.target.value))}
              className="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-xs text-slate-900 focus:bg-white focus:outline-none focus:border-blue-600 shadow-2xs font-medium"
            >
              <option value="1">1 Floor (Ground Only)</option>
              <option value="2">2 Floors (Ground + 1)</option>
              <option value="3">3 Floors (Ground + 2)</option>
            </select>
          </div>

          <div>
            <label className="text-xs font-semibold text-slate-700 block mb-1">
              Masonry Wall Specification
            </label>
            <select
              value={wallType}
              onChange={(e) => setWallType(e.target.value)}
              className="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-xs text-slate-900 focus:bg-white focus:outline-none focus:border-blue-600 shadow-2xs font-medium"
            >
              <option value="AAC Lightweight Blocks">AAC Lightweight Blocks 8&quot;</option>
              <option value="Red Clay Bricks">Wire-cut Red Clay Bricks</option>
            </select>
          </div>

          <div>
            <label className="text-xs font-semibold text-slate-700 block mb-1">
              Construction Quality Tier
            </label>
            <div className="flex gap-2">
              <select
                value={quality}
                onChange={(e) => setQuality(e.target.value)}
                className="flex-1 bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-xs text-slate-900 focus:bg-white focus:outline-none focus:border-blue-600 shadow-2xs font-medium"
              >
                <option value="Economy">Economy</option>
                <option value="Standard">Standard</option>
                <option value="Standard Premium">Standard Premium</option>
                <option value="Luxury">Luxury</option>
              </select>
              <button
                onClick={loadEstimate}
                disabled={isLoading}
                className="px-3.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white transition disabled:opacity-50 shadow-xs"
                title="Calculate"
              >
                <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
              </button>
            </div>
          </div>
        </div>

        {/* Multi-tier Specification Comparison Cards */}
        {comparisons.length > 0 && (
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
            {comparisons.map((c, idx) => (
              <div
                key={idx}
                className={`p-3.5 rounded-xl border transition shadow-2xs ${
                  quality === c.tier
                    ? 'bg-blue-50 border-blue-300 text-blue-900'
                    : 'bg-white border-slate-200 text-slate-700 hover:border-slate-300'
                }`}
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="text-xs font-bold text-slate-900">{c.tier}</span>
                  <span className="text-[10px] text-blue-600 font-mono font-bold">₹{c.rate_sqft}/sqft</span>
                </div>
                <div className="text-base font-extrabold text-slate-900">
                  ₹{(c.total / 100000).toFixed(2)} Lakhs
                </div>
                <p className="text-[10px] text-slate-500 mt-1 line-clamp-1">
                  {c.highlights}
                </p>
              </div>
            ))}
          </div>
        )}

        {/* Cost Breakdown & BOQ Table */}
        {estimate ? (
          <CostBreakdownChart estimate={estimate} />
        ) : (
          <div className="text-center py-20 text-slate-500">
            <Calculator className="w-10 h-10 mx-auto mb-2 text-blue-600 animate-pulse" />
            <p className="text-sm font-medium">Calculating quantities and current market prices...</p>
          </div>
        )}
      </div>
    </div>
  );
}
