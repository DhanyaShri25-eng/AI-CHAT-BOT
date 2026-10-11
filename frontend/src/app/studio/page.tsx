'use client';

import React, { useState, useEffect } from 'react';
import Navbar from '@/components/Navbar';
import FloorPlanCanvas from '@/components/FloorPlanCanvas';
import ElevationPreview from '@/components/ElevationPreview';
import { 
  Layers, 
  RefreshCw, 
  Sliders
} from 'lucide-react';
import { DesignVersion, FloorPlanRoom } from '@/lib/types';
import { generateFloorPlanApi, reviseFloorPlanApi } from '@/lib/api';

export default function ArchitectureStudioPage() {
  const [buildingType, setBuildingType] = useState('3BHK Duplex');
  const [plotWidth, setPlotWidth] = useState(30);
  const [plotLength, setPlotLength] = useState(40);
  const [orientation, setOrientation] = useState('North');
  const [archStyle, setArchStyle] = useState('Modern');
  const [floors, setFloors] = useState(2);
  const [activeTab, setActiveTab] = useState<'floorplan' | 'elevation'>('floorplan');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedRoom, setSelectedRoom] = useState<FloorPlanRoom | null>(null);

  const [design, setDesign] = useState<DesignVersion | null>(null);

  // Generate initial plan on mount
  useEffect(() => {
    loadPlan();
  }, []);

  const loadPlan = async () => {
    setIsLoading(true);
    try {
      const res = await generateFloorPlanApi({
        plot_width: plotWidth,
        plot_length: plotLength,
        building_type: buildingType,
        orientation: orientation,
        floors: floors,
        architectural_style: archStyle
      });
      setDesign(res);
      if (res.rooms && res.rooms.length > 0) {
        setSelectedRoom(res.rooms[0]);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col">
      <Navbar />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 w-full flex-1 flex flex-col space-y-6">
        
        {/* Page Header */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-4 border-b border-slate-200">
          <div>
            <h1 className="text-2xl font-black text-slate-900 flex items-center gap-2.5">
              <span className="p-2 rounded-xl bg-blue-50 border border-blue-200 text-blue-600 shadow-2xs">
                <Layers className="w-5 h-5" />
              </span>
              2D Architecture &amp; Blueprint Studio
            </h1>
            <p className="text-xs text-slate-600 mt-1">
              Parametric geometry engine for setbacks, usable building envelope, room circulation, and Vastu orientation.
            </p>
          </div>

          {/* View Tab Switcher */}
          <div className="flex items-center gap-1.5 p-1 rounded-xl bg-slate-100 border border-slate-200">
            <button
              onClick={() => setActiveTab('floorplan')}
              className={`px-4 py-1.5 rounded-lg text-xs font-semibold transition ${
                activeTab === 'floorplan'
                  ? 'bg-white text-blue-700 border border-blue-200/80 shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              2D Floor Plan Blueprint
            </button>
            <button
              onClick={() => setActiveTab('elevation')}
              className={`px-4 py-1.5 rounded-lg text-xs font-semibold transition ${
                activeTab === 'elevation'
                  ? 'bg-white text-blue-700 border border-blue-200/80 shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Front Elevation Concept
            </button>
          </div>
        </div>

        {/* Main Content Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 flex-1">
          
          {/* Left Controls Column (4 cols) */}
          <div className="lg:col-span-4 space-y-4">
            
            {/* Parameters Panel */}
            <div className="bg-white border border-slate-200 shadow-sm p-5 rounded-2xl space-y-4">
              <h3 className="text-xs font-bold uppercase tracking-wider text-blue-700 flex items-center gap-1.5">
                <Sliders className="w-4 h-4 text-blue-600" />
                Plot &amp; Design Parameters
              </h3>

              {/* Building Type */}
              <div>
                <label className="text-xs font-semibold text-slate-700 block mb-1.5">
                  Building Configuration
                </label>
                <div className="grid grid-cols-3 gap-2">
                  {['1BHK', '2BHK', '3BHK', '4BHK', '3BHK Duplex'].map((type) => (
                    <button
                      key={type}
                      onClick={() => {
                        setBuildingType(type);
                        setFloors(type.includes('Duplex') ? 2 : 1);
                      }}
                      className={`py-1.5 px-2 rounded-lg text-xs font-semibold transition border ${
                        buildingType === type
                          ? 'bg-blue-50 border-blue-300 text-blue-700 shadow-2xs'
                          : 'bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100'
                      }`}
                    >
                      {type}
                    </button>
                  ))}
                </div>
              </div>

              {/* Plot Dimensions */}
              <div className="space-y-3 pt-2">
                <div>
                  <div className="flex justify-between text-xs mb-1">
                    <span className="text-slate-700 font-medium">Plot Width:</span>
                    <span className="text-blue-700 font-mono font-bold">{plotWidth} ft</span>
                  </div>
                  <input
                    type="range"
                    min="20"
                    max="60"
                    value={plotWidth}
                    onChange={(e) => setPlotWidth(Number(e.target.value))}
                    className="w-full accent-blue-600"
                  />
                </div>

                <div>
                  <div className="flex justify-between text-xs mb-1">
                    <span className="text-slate-700 font-medium">Plot Length:</span>
                    <span className="text-blue-700 font-mono font-bold">{plotLength} ft</span>
                  </div>
                  <input
                    type="range"
                    min="30"
                    max="80"
                    value={plotLength}
                    onChange={(e) => setPlotLength(Number(e.target.value))}
                    className="w-full accent-blue-600"
                  />
                </div>
              </div>

              {/* Orientation & Style */}
              <div className="grid grid-cols-2 gap-3 pt-2">
                <div>
                  <label className="text-xs font-semibold text-slate-700 block mb-1">
                    Entrance Facing
                  </label>
                  <select
                    value={orientation}
                    onChange={(e) => setOrientation(e.target.value)}
                    className="w-full bg-slate-50 border border-slate-300 rounded-lg p-2 text-xs text-slate-900 focus:outline-none focus:border-blue-600"
                  >
                    <option value="North">North (Vastu Kubera)</option>
                    <option value="East">East (Vastu Surya)</option>
                    <option value="South">South</option>
                    <option value="West">West</option>
                  </select>
                </div>

                <div>
                  <label className="text-xs font-semibold text-slate-700 block mb-1">
                    Style
                  </label>
                  <select
                    value={archStyle}
                    onChange={(e) => setArchStyle(e.target.value)}
                    className="w-full bg-slate-50 border border-slate-300 rounded-lg p-2 text-xs text-slate-900 focus:outline-none focus:border-blue-600"
                  >
                    <option value="Modern">Modern Minimalist</option>
                    <option value="Contemporary">Contemporary Villa</option>
                    <option value="Traditional">Chettinad Heritage</option>
                    <option value="Kerala">Kerala Vernacular</option>
                  </select>
                </div>
              </div>

              {/* Generate / Regenerate Button */}
              <button
                onClick={loadPlan}
                disabled={isLoading}
                className="w-full flex items-center justify-center gap-2 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs shadow-sm transition disabled:opacity-50 mt-2"
              >
                <RefreshCw className={`w-3.5 h-3.5 ${isLoading ? 'animate-spin' : ''}`} />
                <span>Regenerate Floor Plan</span>
              </button>
            </div>

            {/* Room Inspector Card */}
            {selectedRoom && (
              <div className="bg-white border border-blue-200 shadow-sm p-4 rounded-2xl space-y-2">
                <span className="text-[10px] uppercase font-bold tracking-wider text-blue-700 block">
                  Inspected Room Specification
                </span>
                <div className="flex items-center justify-between">
                  <h4 className="text-sm font-bold text-slate-900">{selectedRoom.name}</h4>
                  <span className="text-xs font-mono font-bold text-blue-700">{selectedRoom.area_sqft} sq.ft</span>
                </div>
                <div className="text-xs text-slate-600 space-y-1 pt-1">
                  <div>Dimensions: <span className="font-mono text-slate-900 font-semibold">{selectedRoom.width}&apos; x {selectedRoom.length}&apos;</span></div>
                  <div>Orientation: <span className="text-blue-700 font-semibold">{selectedRoom.orientation || 'Standard'}</span></div>
                  <div>Floor Level: <span className="text-slate-900 font-semibold">{selectedRoom.floor_level === 0 ? 'Ground Floor' : 'First Floor'}</span></div>
                </div>
              </div>
            )}
          </div>

          {/* Right Main Canvas Column (8 cols) */}
          <div className="lg:col-span-8 flex flex-col min-h-[520px]">
            {activeTab === 'floorplan' && design ? (
              <FloorPlanCanvas
                design={design}
                onRoomSelect={(room) => setSelectedRoom(room)}
              />
            ) : activeTab === 'elevation' && design ? (
              <ElevationPreview
                svgData={design.elevation_data?.svg}
                styleName={archStyle}
                buildingType={buildingType}
                floors={floors}
              />
            ) : (
              <div className="flex-1 flex items-center justify-center bg-white border border-slate-200 shadow-sm rounded-2xl">
                <p className="text-xs text-slate-500 font-medium">Loading architectural models...</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
