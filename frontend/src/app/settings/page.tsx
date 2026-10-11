'use client';

import React, { useState } from 'react';
import Navbar from '@/components/Navbar';
import { 
  Settings, 
  User, 
  Bot, 
  Volume2, 
  Save, 
  Check
} from 'lucide-react';

export default function SettingsPage() {
  const [profile, setProfile] = useState({
    name: 'Sangarsh S',
    email: 'sangarsh@buildwise.ai',
    phone: '+91 98400 12345',
    role: 'Homeowner / Builder',
    location: 'Chennai, Tamil Nadu'
  });

  const [language, setLanguage] = useState('tanglish');
  const [model, setModel] = useState('buildwise-kaggle-census10029-v2.0');
  const [voiceSpeed, setVoiceSpeed] = useState(1.0);
  const [detailLevel, setDetailLevel] = useState('detailed');
  const [saved, setSaved] = useState(false);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    setSaved(true);
    setTimeout(() => setSaved(false), 2500);
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col">
      <Navbar />

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full flex-1 space-y-6">
        
        {/* Header */}
        <div className="flex items-center justify-between pb-4 border-b border-slate-200">
          <div>
            <h1 className="text-2xl font-black text-slate-900 flex items-center gap-2.5">
              <span className="p-2 rounded-xl bg-blue-50 border border-blue-200 text-blue-600 shadow-2xs">
                <Settings className="w-5 h-5" />
              </span>
              Platform Settings &amp; Preferences
            </h1>
            <p className="text-xs text-slate-600 mt-1">
              Configure AI reasoning models, multilingual voice options, and civil engineering defaults.
            </p>
          </div>

          {saved && (
            <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-50 text-emerald-700 text-xs font-semibold border border-emerald-200">
              <Check className="w-4 h-4" /> Preferences Saved!
            </div>
          )}
        </div>

        <form onSubmit={handleSave} className="space-y-6">
          
          {/* User Profile Card */}
          <div className="bg-white border border-slate-200 shadow-sm p-6 rounded-2xl space-y-4">
            <h3 className="text-xs font-bold uppercase tracking-wider text-blue-700 flex items-center gap-2">
              <User className="w-4 h-4 text-blue-600" />
              User Profile
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
              <div>
                <label className="text-slate-700 font-medium block mb-1">Full Name</label>
                <input
                  type="text"
                  value={profile.name}
                  onChange={(e) => setProfile({ ...profile, name: e.target.value })}
                  className="w-full bg-slate-50 border border-slate-300 rounded-xl p-2.5 text-slate-900 focus:bg-white focus:outline-none focus:border-blue-600"
                />
              </div>

              <div>
                <label className="text-slate-700 font-medium block mb-1">Email Address</label>
                <input
                  type="email"
                  value={profile.email}
                  onChange={(e) => setProfile({ ...profile, email: e.target.value })}
                  className="w-full bg-slate-50 border border-slate-300 rounded-xl p-2.5 text-slate-900 focus:bg-white focus:outline-none focus:border-blue-600"
                />
              </div>

              <div>
                <label className="text-slate-700 font-medium block mb-1">Contact Phone</label>
                <input
                  type="text"
                  value={profile.phone}
                  onChange={(e) => setProfile({ ...profile, phone: e.target.value })}
                  className="w-full bg-slate-50 border border-slate-300 rounded-xl p-2.5 text-slate-900 focus:bg-white focus:outline-none focus:border-blue-600"
                />
              </div>

              <div>
                <label className="text-slate-700 font-medium block mb-1">Default Construction Location</label>
                <input
                  type="text"
                  value={profile.location}
                  onChange={(e) => setProfile({ ...profile, location: e.target.value })}
                  className="w-full bg-slate-50 border border-slate-300 rounded-xl p-2.5 text-slate-900 focus:bg-white focus:outline-none focus:border-blue-600"
                />
              </div>
            </div>
          </div>

          {/* AI Reasoning & Model Card */}
          <div className="bg-white border border-slate-200 shadow-sm p-6 rounded-2xl space-y-4">
            <h3 className="text-xs font-bold uppercase tracking-wider text-blue-700 flex items-center gap-2">
              <Bot className="w-4 h-4 text-blue-600" />
              AI Model &amp; Reasoning Settings
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
              <div>
                <label className="text-slate-700 font-medium block mb-1">Active LLM Architecture</label>
                <select
                  value={model}
                  onChange={(e) => setModel(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-300 rounded-xl p-2.5 text-slate-900 font-medium focus:bg-white focus:outline-none focus:border-blue-600"
                >
                  <option value="buildwise-kaggle-census10029-v2.0">
                    BuildWise Kaggle Roof & Census 10029 v2.0
                  </option>
                  <option value="buildwise-kaggle-bubouygues-v1.0">
                    BuildWise Kaggle (Floor Plans & Bouygues)
                  </option>
                  <option value="buildwise-llama3-construction-8b">
                    BuildWise Llama-3 8B (IS 456 Structural Fine-tune)
                  </option>
                  <option value="buildwise-mistral-civil-7b">
                    BuildWise Mistral Civil 7B (Fast CPM Scheduling)
                  </option>
                  <option value="qwen2.5-7b-instruct-local">
                    Qwen 2.5 7B Multilingual Local (Ollama)
                  </option>
                </select>
              </div>

              <div>
                <label className="text-slate-700 font-medium block mb-1">Response Detail Level</label>
                <select
                  value={detailLevel}
                  onChange={(e) => setDetailLevel(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-300 rounded-xl p-2.5 text-slate-900 font-medium focus:bg-white focus:outline-none focus:border-blue-600"
                >
                  <option value="detailed">Comprehensive Engineering (Formulas, IS Codes &amp; BOQ)</option>
                  <option value="concise">Concise Executive Summary</option>
                </select>
              </div>
            </div>
          </div>

          {/* Language & Voice Settings */}
          <div className="bg-white border border-slate-200 shadow-sm p-6 rounded-2xl space-y-4">
            <h3 className="text-xs font-bold uppercase tracking-wider text-blue-700 flex items-center gap-2">
              <Volume2 className="w-4 h-4 text-blue-600" />
              Language &amp; Voice Settings
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
              <div>
                <label className="text-slate-700 font-medium block mb-1">Preferred Input / Speech Language</label>
                <select
                  value={language}
                  onChange={(e) => setLanguage(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-300 rounded-xl p-2.5 text-slate-900 font-medium focus:bg-white focus:outline-none focus:border-blue-600"
                >
                  <option value="tanglish">Tanglish (Tamil + English Mixed e.g. &ldquo;Veedu kattanum&rdquo;)</option>
                  <option value="ta">Tamil (தமிழ்)</option>
                  <option value="en">English (Indian Standard)</option>
                </select>
              </div>

              <div>
                <label className="text-slate-700 font-medium block mb-1">
                  Text-To-Speech Playback Speed ({voiceSpeed}x)
                </label>
                <input
                  type="range"
                  min="0.75"
                  max="1.5"
                  step="0.25"
                  value={voiceSpeed}
                  onChange={(e) => setVoiceSpeed(Number(e.target.value))}
                  className="w-full accent-blue-600 mt-2"
                />
              </div>
            </div>
          </div>

          {/* Save Button */}
          <div className="flex justify-end gap-3 pt-2">
            <button
              type="submit"
              className="flex items-center gap-2 px-6 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold shadow-xs transition"
            >
              <Save className="w-4 h-4" />
              Save Platform Settings
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
