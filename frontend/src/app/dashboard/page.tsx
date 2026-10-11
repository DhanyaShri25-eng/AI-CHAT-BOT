'use client';

import React, { useState, useEffect } from 'react';
import Navbar from '@/components/Navbar';
import Link from 'next/link';
import { 
  Building, 
  MapPin, 
  Layers, 
  Clock
} from 'lucide-react';
import { Project } from '@/lib/types';
import { fetchProjects } from '@/lib/api';

export default function ProjectDashboardPage() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [activeProject, setActiveProject] = useState<Project | null>(null);

  useEffect(() => {
    fetchProjects().then((projs) => {
      setProjects(projs);
      if (projs.length > 0) setActiveProject(projs[0]);
    });
  }, []);

  const stages = [
    { name: 'Planning & Soil Test', status: 'Completed', date: 'Jul 2026' },
    { name: 'Architectural Blueprint', status: 'Completed', date: 'Aug 2026' },
    { name: 'Municipal Plan Sanction', status: 'In Progress', date: 'Sep 2026' },
    { name: 'Foundation & Plinth RCC', status: 'Pending', date: 'Oct 2026' },
    { name: 'RCC Superstructure Slab', status: 'Pending', date: 'Nov 2026' },
    { name: 'Masonry & Plastering', status: 'Pending', date: 'Dec 2026' },
    { name: 'Flooring, Joinery & Painting', status: 'Pending', date: 'Jan 2027' },
    { name: 'Inspection & Griha Pravesham', status: 'Pending', date: 'Feb 2027' },
  ];

  if (!activeProject) {
    return (
      <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col">
        <Navbar />
        <div className="flex-1 flex items-center justify-center">
          <p className="text-slate-500 text-sm font-medium">Loading project dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col">
      <Navbar />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 w-full flex-1 space-y-6">
        
        {/* Project Header Banner */}
        <div className="bg-white border border-slate-200 shadow-sm p-6 rounded-2xl flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="p-2 rounded-xl bg-blue-50 border border-blue-200 text-blue-600 shadow-2xs">
                <Building className="w-5 h-5" />
              </span>
              <h1 className="text-2xl font-black text-slate-900">
                {activeProject.name}
              </h1>
              <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-blue-50 text-blue-700 border border-blue-200">
                Stage: {activeProject.current_stage}
              </span>
            </div>
            <p className="text-xs text-slate-500 flex items-center gap-2">
              <MapPin className="w-3.5 h-3.5 text-slate-400" /> {activeProject.location} • {activeProject.building_type}
            </p>
          </div>

          <div className="flex items-center gap-3">
            <Link
              href="/studio"
              className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold shadow-xs transition"
            >
              <Layers className="w-3.5 h-3.5" /> Open Studio
            </Link>
            <Link
              href="/estimation"
              className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-white hover:bg-slate-50 border border-slate-300 text-slate-700 text-xs font-semibold shadow-2xs transition"
            >
              View BOQ
            </Link>
          </div>
        </div>

        {/* 4 Key Metric Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-white border border-slate-200 shadow-sm p-4 rounded-xl space-y-1">
            <span className="text-[11px] uppercase font-bold tracking-wider text-slate-500">Plot Envelope</span>
            <div className="text-xl font-black text-slate-900 font-mono">
              {activeProject.plot_width}&apos; x {activeProject.plot_length}&apos;
            </div>
            <p className="text-[11px] text-slate-500">
              Total Plot Area: <span className="text-blue-700 font-semibold">{activeProject.plot_area} sq.ft</span>
            </p>
          </div>

          <div className="bg-white border border-slate-200 shadow-sm p-4 rounded-xl space-y-1">
            <span className="text-[11px] uppercase font-bold tracking-wider text-slate-500">Built-Up Area</span>
            <div className="text-xl font-black text-blue-700 font-mono">
              {activeProject.built_up_area} sq.ft
            </div>
            <p className="text-[11px] text-slate-500">
              Across <span className="text-slate-900 font-semibold">{activeProject.floors} Floors</span> • {activeProject.rooms} Rooms
            </p>
          </div>

          <div className="bg-white border border-slate-200 shadow-sm p-4 rounded-xl space-y-1">
            <span className="text-[11px] uppercase font-bold tracking-wider text-slate-500">Target Budget</span>
            <div className="text-xl font-black text-emerald-700 font-mono">
              ₹{(activeProject.target_budget / 100000).toFixed(1)} Lakhs
            </div>
            <p className="text-[11px] text-slate-500">
              Benchmark rate: ~₹{Math.round(activeProject.target_budget / activeProject.built_up_area)}/sq.ft
            </p>
          </div>

          <div className="bg-white border border-slate-200 shadow-sm p-4 rounded-xl space-y-1">
            <span className="text-[11px] uppercase font-bold tracking-wider text-slate-500">Target Handover</span>
            <div className="text-xl font-black text-slate-900">
              Feb 2027
            </div>
            <p className="text-[11px] text-slate-500">
              Estimated 223 Calendar Days
            </p>
          </div>
        </div>

        {/* Milestone Stage Tracker */}
        <div className="bg-white border border-slate-200 shadow-sm p-6 rounded-2xl space-y-4">
          <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider flex items-center gap-2">
            <Clock className="w-4 h-4 text-blue-600" />
            Project Execution Milestones &amp; Gates
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
            {stages.map((stg, idx) => (
              <div
                key={idx}
                className={`p-3.5 rounded-xl border transition ${
                  stg.status === 'Completed'
                    ? 'bg-emerald-50 border-emerald-200 text-emerald-800'
                    : stg.status === 'In Progress'
                    ? 'bg-blue-50 border-blue-300 text-blue-900'
                    : 'bg-slate-50 border-slate-200 text-slate-600'
                }`}
              >
                <div className="flex items-center justify-between mb-1 text-[11px]">
                  <span className="font-mono text-slate-500">Gate 0{idx + 1}</span>
                  <span className="font-semibold">{stg.status}</span>
                </div>
                <h4 className="text-xs font-bold text-slate-900 mb-1">
                  {stg.name}
                </h4>
                <span className="text-[10px] text-slate-500 block font-mono">
                  Target: {stg.date}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
