'use client';

import React, { useState } from 'react';
import { 
  MessageSquare, 
  Plus, 
  Search, 
  Pin, 
  Trash2, 
  ChevronLeft, 
  ChevronRight,
  Bot
} from 'lucide-react';
import { Conversation } from '@/lib/types';

interface SidebarProps {
  conversations: Conversation[];
  activeId?: string;
  onSelect: (id: string) => void;
  onNewChat: () => void;
  onDelete?: (id: string) => void;
  collapsed: boolean;
  onToggleCollapse: () => void;
  selectedModel: string;
  onModelChange: (model: string) => void;
}

export default function Sidebar({
  conversations,
  activeId,
  onSelect,
  onNewChat,
  onDelete,
  collapsed,
  onToggleCollapse,
  selectedModel,
  onModelChange
}: SidebarProps) {
  const [search, setSearch] = useState('');

  const filtered = conversations.filter((c) =>
    c.title.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <aside
      className={`h-[calc(100vh-4rem)] bg-white border-r border-slate-200 transition-all duration-300 flex flex-col z-20 ${
        collapsed ? 'w-14' : 'w-72'
      }`}
    >
      {/* Top Controls */}
      <div className="p-3 border-b border-slate-200 flex items-center justify-between">
        {!collapsed && (
          <button
            onClick={onNewChat}
            className="flex-1 flex items-center justify-center gap-2 px-3 py-2 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold shadow-sm shadow-blue-500/20 transition mr-2"
          >
            <Plus className="w-4 h-4" />
            <span>New Consultation</span>
          </button>
        )}

        <button
          onClick={onToggleCollapse}
          className="p-2 rounded-lg text-slate-500 hover:text-slate-800 hover:bg-slate-100 transition"
          title={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          {collapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
        </button>
      </div>

      {!collapsed && (
        <>
          {/* Search Bar */}
          <div className="p-3 border-b border-slate-200">
            <div className="relative">
              <Search className="w-3.5 h-3.5 absolute left-3 top-2.5 text-slate-400" />
              <input
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search consultations..."
                className="w-full bg-slate-50 border border-slate-200 rounded-lg pl-8 pr-3 py-1.5 text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:bg-white focus:border-blue-500 transition"
              />
            </div>
          </div>

          {/* Model Selector */}
          <div className="px-3 py-2 border-b border-slate-200 bg-slate-50/70">
            <label className="text-[10px] uppercase font-bold tracking-wider text-slate-600 flex items-center gap-1 mb-1">
              <Bot className="w-3 h-3 text-blue-600" />
              Inference Model
            </label>
            <select
              value={selectedModel}
              onChange={(e) => onModelChange(e.target.value)}
              className="w-full bg-white border border-slate-300 rounded-lg px-2 py-1.5 text-xs text-slate-800 font-medium focus:outline-none focus:border-blue-500 shadow-xs"
            >
              <option value="buildwise-kaggle-cubicasa-socal-v3.5">
                🏛️ BuildWise Multi-Dataset Architecture v3.5 (CubiCasa5k + SoCal)
              </option>
              <option value="buildwise-kaggle-census10029-v2.0">
                ⚡ BuildWise Kaggle Roof & Census 10029 v2.0
              </option>
              <option value="buildwise-kaggle-bubouygues-v1.0">
                🚀 BuildWise Kaggle (Floor Plans & Bouygues)
              </option>
              <option value="buildwise-chatgpt-aligned-v1.1">
                🧠 BuildWise ChatGPT-Aligned V1.1 (RLHF)
              </option>
              <option value="buildwise-llama3-construction-8b">
                BuildWise Llama-3 8B (IS 456)
              </option>
              <option value="buildwise-mistral-civil-7b">
                BuildWise Mistral Civil 7B
              </option>
              <option value="qwen2.5-7b-instruct-local">
                Qwen 2.5 7B Local (Ollama)
              </option>
            </select>
          </div>

          {/* Conversation History List */}
          <div className="flex-1 overflow-y-auto p-2 space-y-1">
            <span className="text-[10px] uppercase tracking-wider text-slate-400 font-bold px-2 py-1 block">
              Recent Consultations
            </span>

            {filtered.length === 0 ? (
              <p className="text-xs text-slate-400 px-3 py-4 text-center">
                No conversations found.
              </p>
            ) : (
              filtered.map((c) => {
                const isActive = c.id === activeId;
                return (
                  <div
                    key={c.id}
                    onClick={() => onSelect(c.id)}
                    className={`group flex items-center justify-between px-3 py-2 rounded-xl text-xs cursor-pointer transition ${
                      isActive
                        ? 'bg-blue-50 text-blue-700 font-semibold border border-blue-200 shadow-xs'
                        : 'text-slate-700 hover:bg-slate-100 hover:text-slate-900'
                    }`}
                  >
                    <div className="flex items-center gap-2 truncate">
                      <MessageSquare className={`w-3.5 h-3.5 shrink-0 ${isActive ? 'text-blue-600' : 'text-slate-400'}`} />
                      <span className="truncate">{c.title}</span>
                    </div>

                    <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition">
                      {c.pinned && <Pin className="w-3 h-3 text-amber-500" />}
                      {onDelete && (
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            onDelete(c.id);
                          }}
                          className="p-1 text-slate-400 hover:text-red-500 rounded"
                          title="Delete"
                        >
                          <Trash2 className="w-3 h-3" />
                        </button>
                      )}
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </>
      )}

      {collapsed && (
        <div className="flex flex-col items-center py-4 space-y-3">
          <button
            onClick={onNewChat}
            className="p-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700 transition shadow-sm"
            title="New Chat"
          >
            <Plus className="w-4 h-4" />
          </button>
          <div className="w-8 h-px bg-slate-200" />
          {conversations.slice(0, 5).map((c) => (
            <button
              key={c.id}
              onClick={() => onSelect(c.id)}
              className={`p-2 rounded-lg transition ${
                c.id === activeId ? 'bg-blue-50 text-blue-600 border border-blue-200' : 'text-slate-500 hover:bg-slate-100'
              }`}
              title={c.title}
            >
              <MessageSquare className="w-4 h-4" />
            </button>
          ))}
        </div>
      )}
    </aside>
  );
}
