'use client';

import React, { useState, useEffect } from 'react';
import Navbar from '@/components/Navbar';
import GanttScheduleChart from '@/components/GanttScheduleChart';
import { 
  Calendar, 
  Clock, 
  RefreshCw, 
  CloudRain
} from 'lucide-react';
import { ConstructionSchedule } from '@/lib/types';
import { generateScheduleApi } from '@/lib/api';

export default function TimelinePage() {
  const [builtUpArea, setBuiltUpArea] = useState(1800);
  const [floors, setFloors] = useState(2);
  const [speed, setSpeed] = useState('Normal');
  const [monsoon, setMonsoon] = useState(true);
  const [schedule, setSchedule] = useState<ConstructionSchedule | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    loadSchedule();
  }, []);

  const loadSchedule = async () => {
    setIsLoading(true);
    try {
      const res = await generateScheduleApi({
        built_up_area: builtUpArea,
        floors: floors,
        contractor_speed: speed,
        monsoon_factor: monsoon
      });
      setSchedule(res);
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
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
                <Calendar className="w-5 h-5" />
              </span>
              Critical Path Construction Schedule (CPM)
            </h1>
            <p className="text-xs text-slate-600 mt-1">
              Dependency-linked task scheduling from excavation to Griha Pravesham with weather buffers.
            </p>
          </div>
        </div>

        {/* Schedule Inputs Controls */}
        <div className="bg-white border border-slate-200 shadow-sm p-5 rounded-2xl grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div>
            <label className="text-xs font-semibold text-slate-700 block mb-1">
              Built-up Area (sq.ft)
            </label>
            <input
              type="number"
              value={builtUpArea}
              onChange={(e) => setBuiltUpArea(Number(e.target.value))}
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
              <option value="1">1 Floor (Single Story)</option>
              <option value="2">2 Floors (G+1 Duplex)</option>
              <option value="3">3 Floors (G+2)</option>
            </select>
          </div>

          <div>
            <label className="text-xs font-semibold text-slate-700 block mb-1">
              Contractor Pace
            </label>
            <select
              value={speed}
              onChange={(e) => setSpeed(e.target.value)}
              className="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-xs text-slate-900 focus:bg-white focus:outline-none focus:border-blue-600 shadow-2xs font-medium"
            >
              <option value="Normal">Normal Pace (Standard Quality)</option>
              <option value="Fast-track">Fast-Track (Parallel Gangs)</option>
              <option value="Phased">Phased Budget Release</option>
            </select>
          </div>

          <div>
            <label className="text-xs font-semibold text-slate-700 block mb-1">
              Weather Assumptions
            </label>
            <div className="flex gap-2">
              <button
                onClick={() => setMonsoon(!monsoon)}
                className={`flex-1 py-2 px-3 rounded-xl border text-xs font-semibold flex items-center justify-center gap-1.5 transition shadow-2xs ${
                  monsoon
                    ? 'bg-amber-50 border-amber-300 text-amber-800'
                    : 'bg-slate-50 border-slate-200 text-slate-600'
                }`}
              >
                <CloudRain className="w-3.5 h-3.5" />
                <span>{monsoon ? 'Monsoon Active' : 'Dry Season'}</span>
              </button>
              <button
                onClick={loadSchedule}
                disabled={isLoading}
                className="px-3.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white transition disabled:opacity-50 shadow-xs"
                title="Recalculate Schedule"
              >
                <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
              </button>
            </div>
          </div>
        </div>

        {/* Schedule Gantt View */}
        {schedule ? (
          <GanttScheduleChart schedule={schedule} />
        ) : (
          <div className="text-center py-20 text-slate-500">
            <Clock className="w-10 h-10 mx-auto mb-2 text-blue-600 animate-pulse" />
            <p className="text-sm font-medium">Calculating CPM sequence and task dependency graph...</p>
          </div>
        )}
      </div>
    </div>
  );
}
