'use client';

import React from 'react';
import { Layers, Download, Ruler } from 'lucide-react';

interface ElevationPreviewProps {
  svgData?: string;
  styleName?: string;
  buildingType?: string;
  floors?: number;
}

export default function ElevationPreview({
  svgData,
  styleName = 'Modern',
  buildingType = '3BHK Duplex',
  floors = 2
}: ElevationPreviewProps) {
  const downloadElevation = () => {
    if (!svgData) return;
    const blob = new Blob([svgData], { type: 'image/svg+xml' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `buildwise-front-elevation-${styleName.toLowerCase()}.svg`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 bg-slate-50 border-b border-slate-200">
        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded-lg bg-blue-50 border border-blue-200 text-blue-600">
            <Layers className="w-4 h-4" />
          </div>
          <div>
            <h4 className="text-xs font-bold text-slate-900 tracking-wide uppercase">
              Architectural Front Elevation Concept
            </h4>
            <p className="text-[11px] text-slate-500">
              Style: <span className="text-blue-700 font-semibold">{styleName}</span> | {floors} Floor(s) | {buildingType}
            </p>
          </div>
        </div>

        <button
          onClick={downloadElevation}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-white hover:bg-slate-50 border border-slate-300 text-slate-700 text-xs font-semibold transition shadow-2xs"
        >
          <Download className="w-3.5 h-3.5 text-blue-600" />
          Export Concept
        </button>
      </div>

      {/* SVG Viewport */}
      <div className="p-6 flex items-center justify-center min-h-[380px] bg-slate-50">
        {svgData ? (
          <div
            className="w-full max-w-[640px] rounded-xl overflow-hidden border border-slate-200 shadow-md bg-white p-2"
            dangerouslySetInnerHTML={{ __html: svgData }}
          />
        ) : (
          <div className="text-center text-slate-400">
            <Ruler className="w-8 h-8 mx-auto mb-2 text-blue-600" />
            <p className="text-xs font-medium">Elevation concept rendering in progress...</p>
          </div>
        )}
      </div>

      {/* Elevation Specs Footer */}
      <div className="px-4 py-3 bg-white border-t border-slate-200 grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs text-slate-700">
        <div>
          <span className="text-[10px] text-slate-500 block uppercase font-medium">Plinth Height</span>
          <span className="font-semibold text-slate-900">+2.5 ft above road</span>
        </div>
        <div>
          <span className="text-[10px] text-slate-500 block uppercase font-medium">Ceiling Clearance</span>
          <span className="font-semibold text-slate-900">10.5 ft floor-to-floor</span>
        </div>
        <div>
          <span className="text-[10px] text-slate-500 block uppercase font-medium">Parapet Wall</span>
          <span className="font-semibold text-slate-900">3.5 ft safety railing</span>
        </div>
        <div>
          <span className="text-[10px] text-slate-500 block uppercase font-medium">Glazing Spec</span>
          <span className="font-semibold text-blue-700">Toughened French glass</span>
        </div>
      </div>
    </div>
  );
}
