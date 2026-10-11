'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import Navbar from '@/components/Navbar';
import { 
  Compass, 
  Sparkles, 
  Layers, 
  Calculator, 
  Calendar, 
  Mic, 
  ShieldCheck, 
  ArrowRight, 
  FileSpreadsheet
} from 'lucide-react';

export default function LandingPage() {
  const [selectedExample, setSelectedExample] = useState(
    '30x40 plot la 3BHK duplex veedu kattanum, budget 45 lakhs, vadakku paatha vaasal venum'
  );

  const samplePrompts = [
    {
      title: '30x40 Duplex (Tamil / Tanglish)',
      text: '30x40 plot la 3BHK duplex veedu kattanum, budget 45 lakhs, vadakku paatha vaasal venum'
    },
    {
      title: '2BHK Single Floor Budget Plan',
      text: 'Generate a 2BHK Vastu-compliant layout for 25x50 East facing plot with car parking'
    },
    {
      title: 'Commercial / Multi-Unit G+2',
      text: 'Calculate IS 456 cement and steel quantities for G+2 residential apartment on 2400 sq.ft plot'
    },
    {
      title: 'TNCDBR Setback & FSI Verification',
      text: 'What are the mandatory front and rear setbacks for 30ft road under Tamil Nadu Building Rules 2019?'
    }
  ];

  const features = [
    {
      icon: Layers,
      title: '2D Architectural Floor-Plan Studio',
      description: 'Generates deterministic room layouts, boundary setbacks, circulation checks, and architectural front elevations in scaled blueprint SVG format.'
    },
    {
      icon: Calculator,
      title: 'IS 456 Material Calculation Engine',
      description: 'Calculates exact cement bags, steel rebar tonnage, M-sand, aggregate, bricks, and tiles based on National Building Code structural thumb-rules.'
    },
    {
      icon: FileSpreadsheet,
      title: 'Itemized Cost Estimation Engine',
      description: 'Provides low, expected, and high budgets itemized across civil materials, labour wages, equipment, statutory plan sanctions, and contingency.'
    },
    {
      icon: Calendar,
      title: 'CPM Construction Scheduling',
      description: 'Dependency-aware Critical Path Method scheduling with 15 execution gates, Gantt chart timeline, and monsoon delay risk mitigation.'
    },
    {
      icon: Mic,
      title: 'Voice-Enabled Tamil & Tanglish',
      description: 'Speak naturally in English, Tamil, or Tanglish. BuildWise transcribes your voice and extracts plot dimensions, budgets, and Vastu needs.'
    },
    {
      icon: ShieldCheck,
      title: 'Verified Regulatory RAG',
      description: 'Grounds every design and setback recommendation in verified National Building Code (NBC 2016) and Tamil Nadu Combined Building Rules (TNCDBR).'
    }
  ];

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col selection:bg-blue-600 selection:text-white">
      <Navbar />

      {/* Hero Section with Light Blueprint Styling */}
      <section className="relative pt-20 pb-24 overflow-hidden blueprint-grid-bg border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center">
          
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-blue-50 border border-blue-200 text-blue-700 text-xs font-semibold mb-6 shadow-xs">
            <Sparkles className="w-3.5 h-3.5 text-blue-600" />
            <span>AI Platform for Civil Architecture & Construction Costing</span>
          </div>

          {/* Heading */}
          <h1 className="text-4xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight text-slate-900 max-w-4xl mx-auto leading-tight">
            Design, Estimate &amp; Plan Your Building with{' '}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 via-sky-600 to-indigo-600">
              BuildWise AI
            </span>
          </h1>

          <p className="mt-6 text-base sm:text-lg text-slate-600 max-w-2xl mx-auto leading-relaxed">
            The civil engineering AI platform that generates Vastu-compliant 2D floor plans, 
            deterministic IS 456 material quantities, itemized construction budgets, and Gantt schedules.
          </p>

          {/* CTA Buttons */}
          <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              href="/chat"
              className="w-full sm:w-auto flex items-center justify-center gap-2 px-8 py-3.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm shadow-lg shadow-blue-500/20 transition-all hover:scale-105"
            >
              <Sparkles className="w-4 h-4" />
              <span>Start Building Now</span>
              <ArrowRight className="w-4 h-4" />
            </Link>

            <Link
              href="/studio"
              className="w-full sm:w-auto flex items-center justify-center gap-2 px-7 py-3.5 rounded-xl bg-white hover:bg-slate-50 border border-slate-300 text-slate-800 font-semibold text-sm transition shadow-xs"
            >
              <Layers className="w-4 h-4 text-blue-600" />
              <span>Explore Architecture Studio</span>
            </Link>
          </div>

          {/* Interactive Example Prompts Strip */}
          <div className="mt-12 max-w-3xl mx-auto text-left">
            <span className="text-xs uppercase font-bold tracking-wider text-slate-500 block mb-2 text-center sm:text-left">
              Try Example Construction Prompts:
            </span>
            <div className="flex flex-wrap gap-2 justify-center sm:justify-start">
              {samplePrompts.map((p, idx) => (
                <button
                  key={idx}
                  onClick={() => setSelectedExample(p.text)}
                  className={`text-xs px-3 py-1.5 rounded-lg border transition ${
                    selectedExample === p.text
                      ? 'bg-blue-50 border-blue-300 text-blue-700 font-semibold'
                      : 'bg-white border-slate-200 text-slate-600 hover:border-slate-300'
                  }`}
                >
                  {p.title}
                </button>
              ))}
            </div>

            {/* Selected Prompt Action Box */}
            <div className="mt-4 p-4 rounded-xl bg-white border border-slate-200 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 shadow-sm">
              <p className="text-xs text-slate-800 font-mono italic">
                &ldquo;{selectedExample}&rdquo;
              </p>
              <Link
                href={`/chat?prompt=${encodeURIComponent(selectedExample)}`}
                className="shrink-0 flex items-center gap-1.5 px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold shadow-xs transition"
              >
                <span>Consult AI</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Feature Grid */}
      <section className="py-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h2 className="text-xs uppercase font-bold tracking-widest text-blue-600 mb-2">
            Engineering Precision
          </h2>
          <p className="text-3xl font-extrabold text-slate-900">
            Built for Architects, Engineers, and Homeowners
          </p>
          <p className="text-sm text-slate-600 mt-2">
            Every feature connects to real mathematical calculation engines, statutory by-laws, and structural engineering codes.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feat, idx) => {
            const Icon = feat.icon;
            return (
              <div
                key={idx}
                className="bg-white border border-slate-200 hover:border-blue-300 p-6 rounded-2xl flex flex-col justify-between transition-all hover:-translate-y-1 shadow-xs hover:shadow-md"
              >
                <div>
                  <div className="w-12 h-12 rounded-xl bg-blue-50 border border-blue-200 text-blue-600 flex items-center justify-center mb-4 shadow-2xs">
                    <Icon className="w-6 h-6" />
                  </div>
                  <h3 className="text-base font-bold text-slate-900 mb-2">
                    {feat.title}
                  </h3>
                  <p className="text-xs text-slate-600 leading-relaxed">
                    {feat.description}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* Footer */}
      <footer className="mt-auto border-t border-slate-200 bg-white py-8 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <Compass className="w-4 h-4 text-blue-600" />
            <span className="font-bold text-slate-900">BuildWise AI</span>
            <span>• Full-Stack Architectural Intelligence</span>
          </div>
          <div className="flex items-center gap-4 text-slate-500">
            <span>IS 456:2000 Compliant</span>
            <span>•</span>
            <span>NBC 2016 Standards</span>
            <span>•</span>
            <span>Tamil Nadu TNCDBR 2019</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
