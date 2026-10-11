'use client';

import React from 'react';
import { 
  TrendingUp, 
  ShieldCheck, 
  FileSpreadsheet
} from 'lucide-react';
import { CostEstimate } from '@/lib/types';

interface CostBreakdownChartProps {
  estimate: CostEstimate;
}

export default function CostBreakdownChart({ estimate }: CostBreakdownChartProps) {
  const formatCurrency = (val: number) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0
    }).format(val);
  };

  const phases = Object.entries(estimate.breakdown_by_phase || {});

  return (
    <div className="space-y-6">
      {/* 3 Metric Cards: Low, Expected, High */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Low Estimate */}
        <div className="bg-white border border-slate-200 shadow-sm p-5 rounded-2xl relative overflow-hidden">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs uppercase font-bold tracking-wider text-slate-500">Low Estimate</span>
            <span className="text-[11px] px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-700 font-semibold border border-emerald-200">Value Engineering</span>
          </div>
          <div className="text-2xl font-black text-slate-900">
            {formatCurrency(estimate.total_low)}
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Standard specifications, bulk local procurement.
          </p>
        </div>

        {/* Expected Estimate (Hero) */}
        <div className="bg-white border-2 border-blue-500 shadow-md p-5 rounded-2xl relative overflow-hidden">
          <div className="absolute top-0 right-0 w-24 h-24 bg-blue-50 rounded-full blur-2xl pointer-events-none" />
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs uppercase font-bold tracking-wider text-blue-700">Expected Budget</span>
            <span className="text-[11px] px-2.5 py-0.5 rounded-full bg-blue-50 text-blue-700 font-bold border border-blue-200">Benchmark Rate</span>
          </div>
          <div className="text-3xl font-black text-blue-600">
            {formatCurrency(estimate.total_expected)}
          </div>
          <div className="flex items-center gap-2 mt-1.5 text-xs text-slate-700 font-semibold">
            <span>₹{Math.round(estimate.rate_per_sqft)} / sq.ft</span>
            <span>•</span>
            <span>All Taxes & Labour Included</span>
          </div>
        </div>

        {/* High Estimate */}
        <div className="bg-white border border-slate-200 shadow-sm p-5 rounded-2xl relative overflow-hidden">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs uppercase font-bold tracking-wider text-slate-500">High Estimate</span>
            <span className="text-[11px] px-2.5 py-0.5 rounded-full bg-amber-50 text-amber-700 font-semibold border border-amber-200">Premium Finishes</span>
          </div>
          <div className="text-2xl font-black text-slate-900">
            {formatCurrency(estimate.total_high)}
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Imported tiles, teak wood, premium fittings.
          </p>
        </div>
      </div>

      {/* Itemized Phase Breakdown Bars */}
      <div className="bg-white border border-slate-200 shadow-sm p-6 rounded-2xl">
        <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider mb-4 flex items-center gap-2">
          <TrendingUp className="w-4 h-4 text-blue-600" />
          Construction Cost Breakdown by Engineering Phase
        </h3>

        <div className="space-y-3.5">
          {phases.map(([phaseName, amount]) => {
            const percentage = Math.round((amount / estimate.total_expected) * 100);
            return (
              <div key={phaseName} className="space-y-1">
                <div className="flex items-center justify-between text-xs">
                  <span className="text-slate-800 font-semibold">{phaseName}</span>
                  <div className="flex items-center gap-2">
                    <span className="text-slate-500 font-mono text-[11px]">{percentage}%</span>
                    <span className="text-blue-700 font-bold font-mono">{formatCurrency(amount)}</span>
                  </div>
                </div>
                <div className="w-full h-2 rounded-full bg-slate-100 overflow-hidden">
                  <div
                    className="h-full bg-blue-600 rounded-full transition-all duration-500"
                    style={{ width: `${Math.max(percentage, 3)}%` }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Detailed Material Quantities & Specifications Table */}
      <div className="bg-white border border-slate-200 shadow-sm rounded-2xl overflow-hidden">
        <div className="p-4 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
          <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider flex items-center gap-2">
            <FileSpreadsheet className="w-4 h-4 text-blue-600" />
            Deterministic Material Quantities (IS 456 & NBC Code)
          </h3>
          <span className="text-[11px] text-emerald-700 flex items-center gap-1 font-semibold">
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
            Engineering Wastage Factored
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 text-slate-600 uppercase text-[10px] tracking-wider border-b border-slate-200">
              <tr>
                <th className="px-4 py-3 font-semibold">Material Specification</th>
                <th className="px-3 py-3 font-semibold">Base Qty</th>
                <th className="px-3 py-3 font-semibold">Wastage</th>
                <th className="px-3 py-3 font-semibold">Procurement Qty</th>
                <th className="px-3 py-3 font-semibold">Unit Rate</th>
                <th className="px-4 py-3 font-semibold text-right">Total Amount</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {estimate.breakdown_by_material?.map((mat, idx) => (
                <tr key={idx} className="hover:bg-blue-50/50 transition">
                  <td className="px-4 py-3">
                    <div className="font-semibold text-slate-900">{mat.name}</div>
                    <div className="text-[10px] text-slate-500">{mat.calculation_method}</div>
                  </td>
                  <td className="px-3 py-3 text-slate-700 font-mono">
                    {mat.estimated_quantity} {mat.unit}
                  </td>
                  <td className="px-3 py-3 text-amber-600 font-mono font-medium">
                    +{mat.wastage_percent}%
                  </td>
                  <td className="px-3 py-3 text-blue-700 font-bold font-mono">
                    {mat.procurement_quantity} {mat.unit}
                  </td>
                  <td className="px-3 py-3 text-slate-700 font-mono">
                    ₹{mat.unit_price.toLocaleString()}
                  </td>
                  <td className="px-4 py-3 text-right font-bold text-slate-900 font-mono">
                    {formatCurrency(mat.total_cost)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
