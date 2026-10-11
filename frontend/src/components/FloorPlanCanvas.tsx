'use client';

import React, { useState } from 'react';
import { 
  ZoomIn, 
  ZoomOut, 
  RotateCcw, 
  Download, 
  Compass, 
  Info,
  CheckCircle2
} from 'lucide-react';
import { DesignVersion, FloorPlanRoom } from '@/lib/types';

interface FloorPlanCanvasProps {
  design: DesignVersion;
  onRoomSelect?: (room: FloorPlanRoom) => void;
}

export default function FloorPlanCanvas({ design, onRoomSelect }: FloorPlanCanvasProps) {
  const [zoom, setZoom] = useState(1.0);
  const [selectedRoom, setSelectedRoom] = useState<FloorPlanRoom | null>(null);

  const handleZoomIn = () => setZoom((prev) => Math.min(prev + 0.15, 2.0));
  const handleZoomOut = () => setZoom((prev) => Math.max(prev - 0.15, 0.6));
  const handleResetZoom = () => setZoom(1.0);

  const downloadSvg = () => {
    if (!design.svg_data) return;
    const blob = new Blob([design.svg_data], { type: 'image/svg+xml' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `buildwise-blueprint-${design.version_number}.svg`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="flex flex-col h-full bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm relative">
      {/* Top Toolbar */}
      <div className="flex items-center justify-between px-4 py-3 bg-slate-50 border-b border-slate-200">
        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded-lg bg-blue-50 border border-blue-200 text-blue-600">
            <Compass className="w-4 h-4" />
          </div>
          <div>
            <h4 className="text-xs font-bold text-slate-900 tracking-wide uppercase">
              {design.title}
            </h4>
            <p className="text-[11px] text-slate-500">
              Built-up: <span className="text-blue-700 font-semibold">{design.total_area_sqft} sq.ft</span> | 
              Plot: <span className="text-slate-800 font-medium">{design.plot_boundary.plot_width}&apos; x {design.plot_boundary.plot_length}&apos;</span>
            </p>
          </div>
        </div>

        {/* Controls */}
        <div className="flex items-center gap-1.5">
          <button
            onClick={handleZoomIn}
            className="p-1.5 rounded-md bg-white border border-slate-200 text-slate-700 hover:text-slate-900 hover:bg-slate-100 transition shadow-2xs"
            title="Zoom In"
          >
            <ZoomIn className="w-4 h-4" />
          </button>
          <button
            onClick={handleZoomOut}
            className="p-1.5 rounded-md bg-white border border-slate-200 text-slate-700 hover:text-slate-900 hover:bg-slate-100 transition shadow-2xs"
            title="Zoom Out"
          >
            <ZoomOut className="w-4 h-4" />
          </button>
          <button
            onClick={handleResetZoom}
            className="p-1.5 rounded-md bg-white border border-slate-200 text-slate-700 hover:text-slate-900 hover:bg-slate-100 transition shadow-2xs"
            title="Reset Zoom"
          >
            <RotateCcw className="w-4 h-4" />
          </button>
          <span className="text-[11px] text-slate-600 font-mono px-2 font-medium">
            {Math.round(zoom * 100)}%
          </span>
          <button
            onClick={downloadSvg}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold transition shadow-xs ml-2"
          >
            <Download className="w-3.5 h-3.5" />
            Export SVG
          </button>
        </div>
      </div>

      {/* Main Blueprint Viewport */}
      <div className="flex-1 overflow-auto flex items-center justify-center p-6 relative blueprint-grid-bg min-h-[460px]">
        {design.svg_data ? (
          <div
            style={{ transform: `scale(${zoom})`, transformOrigin: 'center center', transition: 'transform 0.15s ease-out' }}
            className="rounded-lg shadow-md border border-slate-200 max-w-full max-h-full bg-white p-2"
            dangerouslySetInnerHTML={{ __html: design.svg_data }}
          />
        ) : (
          <div className="text-center text-slate-400">
            <Info className="w-10 h-10 mx-auto mb-2 text-blue-600 animate-pulse" />
            <p className="text-sm font-medium">Generating floor plan blueprint...</p>
          </div>
        )}

        {/* Architectural Setback Badge Overlay */}
        <div className="absolute top-4 left-4 bg-white/95 backdrop-blur-md border border-slate-200 rounded-lg p-2.5 text-[11px] text-slate-700 pointer-events-none shadow-sm">
          <div className="text-blue-700 font-bold mb-1 flex items-center gap-1">
            <CheckCircle2 className="w-3.5 h-3.5" /> Municipal Setbacks Verified
          </div>
          <div className="space-y-0.5 text-slate-600">
            <div>Front: {design.plot_boundary.setback_front}&apos; (Road frontage)</div>
            <div>Rear: {design.plot_boundary.setback_rear}&apos; | Sides: {design.plot_boundary.setback_sides}&apos;</div>
            <div className="text-slate-900 font-mono font-semibold pt-1">Envelope: {design.plot_boundary.usable_width.toFixed(1)}&apos; x {design.plot_boundary.usable_length.toFixed(1)}&apos;</div>
          </div>
        </div>
      </div>

      {/* Room Selection Strip */}
      <div className="bg-white border-t border-slate-200 px-4 py-2.5 flex items-center gap-2 overflow-x-auto">
        <span className="text-[11px] uppercase tracking-wider text-slate-500 font-bold shrink-0">
          Rooms:
        </span>
        {design.rooms.map((room) => (
          <button
            key={room.id}
            onClick={() => {
              setSelectedRoom(room);
              onRoomSelect?.(room);
            }}
            className={`px-3 py-1 rounded-md text-xs whitespace-nowrap transition border ${
              selectedRoom?.id === room.id
                ? 'bg-blue-50 border-blue-300 text-blue-700 font-bold shadow-2xs'
                : 'bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100'
            }`}
          >
            {room.name} <span className="text-slate-500 text-[10px]">({room.area_sqft} sq.ft)</span>
          </button>
        ))}
      </div>
    </div>
  );
}
