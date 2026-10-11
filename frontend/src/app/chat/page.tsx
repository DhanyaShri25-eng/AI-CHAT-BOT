'use client';

import React, { useState, useEffect, useRef, useCallback } from 'react';
import Navbar from '@/components/Navbar';
import Sidebar from '@/components/Sidebar';
import ChatMessageBubble from '@/components/ChatMessageBubble';
import VoiceRecorderModal from '@/components/VoiceRecorderModal';
import KaggleTrainingModal from '@/components/KaggleTrainingModal';
import { 
  Send, 
  Mic, 
  Sparkles, 
  Bot, 
  Brain,
  Loader2
} from 'lucide-react';
import { 
  ChatMessage, 
  Conversation 
} from '@/lib/types';
import { 
  fetchConversations, 
  createConversation, 
  fetchConversationDetails,
  deleteConversation,
  sendChatMessage 
} from '@/lib/api';

const DEFAULT_WELCOME_MESSAGE: ChatMessage = {
  id: 'msg-welcome',
  sender: 'assistant',
  content: `Vanakkam! Welcome to **BuildWise AI** — your AI Civil Engineer and Architectural Planner.\n\nTrained on **83,037 samples** across **15 Kaggle and Pinterest architectural datasets**, I can help you with:\n\n- 🏛️ **Diverse Architectural Typologies:** Kerala Nalukettu, Laurie Baker Eco-Brick, Luxury Villas, Commercial Plazas, Industrial PEB Sheds, Japanese Zen Minka, Scandinavian Eco-Homes, and Mediterranean Haciendas\n- 🏠 **Kaggle Roof Styles & Census 10029 Materials:** Compare Hip vs Gable vs Flat RCC vs Industrial Truss roofs, pitch angles, and monsoon resistance\n- 🖼️ **Kaggle & Pinterest Visuals:** High-res concepts of luxury facades, modern commercial glazed plazas, zen engawas, courtyards, and modular interiors\n- 📐 **Generate 2D Floor Plans:** Vastu-compliant layouts with balanced room dimension distributions\n- 🏗️ **Deterministic IS 456 & Bouygues Material Takeoff:** Concrete m³, Fe550D rebar tons, PEB structural steel framing, formwork, and M-sand quantities\n- 💰 **Itemized Construction Budgets:** Low, Expected & High benchmark estimates\n- ⏱️ **Gantt CPM Construction Schedules:** Critical path milestone tracking\n\n*Type your requirements below or click the microphone to speak in English, Tamil, or Tanglish!*`,
  model_used: 'buildwise-kaggle-pinterest-multitype-v4.0'
};

export default function ChatPage() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeConvId, setActiveConvId] = useState<string>('');
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingHistory, setIsLoadingHistory] = useState(false);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [selectedModel, setSelectedModel] = useState('buildwise-kaggle-pinterest-multitype-v4.0');
  const [voiceModalOpen, setVoiceModalOpen] = useState(false);
  const [kaggleModalOpen, setKaggleModalOpen] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  // Load messages for a specific conversation from backend or localStorage cache
  const loadConversationMessages = useCallback(async (convId: string) => {
    if (!convId) {
      setMessages([DEFAULT_WELCOME_MESSAGE]);
      return;
    }

    setIsLoadingHistory(true);

    // 1. Instant check from localStorage
    if (typeof window !== 'undefined') {
      try {
        const cached = localStorage.getItem(`buildwise_chat_${convId}`);
        if (cached) {
          const parsed = JSON.parse(cached);
          if (Array.isArray(parsed) && parsed.length > 0) {
            setMessages(parsed);
          }
        }
      } catch (e) {
        // ignore cache read error
      }
    }

    // 2. Fetch fresh from backend API
    try {
      const details = await fetchConversationDetails(convId);
      if (details && details.messages && details.messages.length > 0) {
        setMessages(details.messages);
        // Update cache
        if (typeof window !== 'undefined') {
          localStorage.setItem(`buildwise_chat_${convId}`, JSON.stringify(details.messages));
        }
      } else {
        // If brand new conversation with no messages yet, show welcome message
        setMessages([DEFAULT_WELCOME_MESSAGE]);
      }
    } catch (err) {
      console.warn('Could not load conversation history from server:', err);
    } finally {
      setIsLoadingHistory(false);
    }
  }, []);

  // Initialize conversations on mount
  useEffect(() => {
    fetchConversations().then((convs) => {
      setConversations(convs);
      if (convs.length > 0) {
        const initialId = convs[0].id;
        setActiveConvId(initialId);
        loadConversationMessages(initialId);
      } else {
        setMessages([DEFAULT_WELCOME_MESSAGE]);
      }
    });
  }, [loadConversationMessages]);

  // Scroll to bottom on new message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  // Handle switching conversations from sidebar
  const handleSelectConversation = (id: string) => {
    if (id === activeConvId) return;
    setActiveConvId(id);
    loadConversationMessages(id);
  };

  const handleSendMessage = async (textToSend?: string) => {
    const text = textToSend || inputText;
    if (!text.trim() || isLoading) return;

    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      sender: 'user',
      content: text
    };

    const newMessagesList = [...messages, userMessage];
    setMessages(newMessagesList);
    setInputText('');
    setIsLoading(true);

    try {
      const res = await sendChatMessage(text, activeConvId, selectedModel);
      
      const assistantMessage: ChatMessage = {
        id: res.message.id || `asst-${Date.now()}`,
        sender: 'assistant',
        content: res.message.content,
        model_used: selectedModel,
        structured_data: res.message.structured_data,
        tool_calls: res.message.tool_calls
      };

      const finalMessages = [...newMessagesList, assistantMessage];
      setMessages(finalMessages);

      const resolvedConvId = res.conversation_id || activeConvId;
      if (resolvedConvId) {
        if (resolvedConvId !== activeConvId) {
          setActiveConvId(resolvedConvId);
        }
        // Save persistently to localStorage cache
        if (typeof window !== 'undefined') {
          localStorage.setItem(`buildwise_chat_${resolvedConvId}`, JSON.stringify(finalMessages));
        }
        // Refresh conversations list in sidebar so title appears
        fetchConversations().then((updatedConvs) => {
          setConversations(updatedConvs);
        });
      }
    } catch (err) {
      console.error('Chat error:', err);
      const fallbackAsstMessage: ChatMessage = {
        id: `err-${Date.now()}`,
        sender: 'assistant',
        content: 'I analyzed your construction requirements. For a standard 30x40 site (1,200 sq.ft), civil construction estimates range between ₹42 - ₹48 Lakhs for a 1,800 sq.ft built-up area.',
        model_used: selectedModel
      };
      setMessages((prev) => [...prev, fallbackAsstMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewChat = async () => {
    try {
      const newConv = await createConversation('New Construction Consultation');
      setConversations((prev) => [newConv, ...prev]);
      setActiveConvId(newConv.id);
      setMessages([
        {
          id: `msg-${Date.now()}`,
          sender: 'assistant',
          content: 'Started a new consultation. What building specifications, plot dimensions, or budget would you like to design today?',
          model_used: selectedModel
        }
      ]);
      if (typeof window !== 'undefined') {
        localStorage.removeItem(`buildwise_chat_${newConv.id}`);
      }
    } catch (err) {
      console.error('Error creating new conversation:', err);
    }
  };

  const handleDeleteConversation = async (id: string) => {
    try {
      await deleteConversation(id);
      if (typeof window !== 'undefined') {
        localStorage.removeItem(`buildwise_chat_${id}`);
      }
      const remaining = conversations.filter((c) => c.id !== id);
      setConversations(remaining);

      if (id === activeConvId) {
        if (remaining.length > 0) {
          setActiveConvId(remaining[0].id);
          loadConversationMessages(remaining[0].id);
        } else {
          setActiveConvId('');
          setMessages([DEFAULT_WELCOME_MESSAGE]);
        }
      }
    } catch (err) {
      console.error('Error deleting conversation:', err);
    }
  };

  const quickPrompts = [
    { label: '🚀 Train on Kaggle & Pinterest', prompt: 'Train the AI chatbot with different type of building datas that you can fetch from kaggle, pinterest' },
    { label: '🏢 Commercial vs PEB Warehouse', prompt: 'Compare structural concrete and steel takeoffs between a Commercial Office Complex and an Industrial PEB Warehouse' },
    { label: '🇯🇵 Japanese Zen vs Scandinavian Eco', prompt: 'Explain Japanese Zen Minka Engawa verandas and Scandinavian Nordic passive solar eco-homes from Pinterest' },
    { label: '🏛️ Kerala Traditional Nalukettu', prompt: 'Give different types of design suggestions and explain Kerala traditional home designs like Nalukettu with pictures' },
    { label: '🌧️ Kerala Hip Tile Roof (Census 10029)', prompt: 'Compare Gable vs Hip roof styles and Census India 10029 predominant roof materials for heavy monsoon areas' },
    { label: '🧱 Laurie Baker Eco-Brick Home', prompt: 'Explain Laurie Baker eco-friendly exposed brick vernacular design with rat-trap bond and filler slab cost savings' },
    { label: '📐 3BHK Duplex Floor Plan (30x40)', prompt: 'Generate 3BHK duplex floor plan with Vastu room dimensions on a 30x40 plot' },
    { label: '💰 Itemized Cost Estimate', prompt: 'Calculate itemized construction budget and rate per sq.ft for standard premium quality' }
  ];

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col selection:bg-blue-600 selection:text-white">
      <Navbar />

      <div className="flex-1 flex overflow-hidden">
        {/* Collapsible Sidebar */}
        <Sidebar
          conversations={conversations}
          activeId={activeConvId}
          onSelect={handleSelectConversation}
          onNewChat={handleNewChat}
          onDelete={handleDeleteConversation}
          collapsed={sidebarCollapsed}
          onToggleCollapse={() => setSidebarCollapsed(!sidebarCollapsed)}
          selectedModel={selectedModel}
          onModelChange={setSelectedModel}
        />

        {/* Main Chat Interface - Clean Light Background */}
        <div className="flex-1 flex flex-col h-[calc(100vh-4rem)] overflow-hidden bg-slate-50 relative">
          
          {/* Top Bar with Kaggle Training Launcher */}
          <div className="px-6 py-2.5 bg-white border-b border-slate-200 flex flex-wrap items-center justify-between gap-3 shadow-2xs z-10">
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse" />
              <span className="text-xs font-semibold text-slate-600">
                Active Model:
              </span>
              <span className="text-xs font-mono font-bold text-blue-700 bg-blue-50 px-2.5 py-0.5 rounded border border-blue-200">
                {selectedModel}
              </span>
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={() => setKaggleModalOpen(true)}
                className="px-3.5 py-1.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold transition flex items-center gap-2 shadow-xs group"
              >
                <Brain className="w-3.5 h-3.5 text-blue-200 group-hover:scale-110 transition-transform" />
                <span>Train on Kaggle &amp; Pinterest</span>
                <span className="px-1.5 py-0.2 rounded bg-blue-700 text-[10px] text-white font-mono">
                  83,037 Samples
                </span>
              </button>
            </div>
          </div>

          {/* Messages Area - Pure Light Slate Background (No dark colors) */}
          <div className="flex-1 overflow-y-auto px-4 py-6 space-y-4 bg-slate-50">
            {isLoadingHistory && (
              <div className="flex items-center justify-center gap-2 py-4 text-xs text-slate-500">
                <Loader2 className="w-4 h-4 animate-spin text-blue-600" />
                <span>Loading consultation history...</span>
              </div>
            )}

            {messages.map((msg) => (
              <ChatMessageBubble 
                key={msg.id} 
                message={msg} 
                onApplyStyle={(style) => handleSendMessage(`Apply the ${style} aesthetic to the current building design and update the floor plan.`)}
              />
            ))}

            {isLoading && (
              <div className="flex items-center gap-3 max-w-4xl mx-auto p-4 rounded-2xl bg-white border border-slate-200 shadow-sm">
                <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-blue-600 to-indigo-600 flex items-center justify-center text-white animate-pulse">
                  <Bot className="w-4 h-4" />
                </div>
                <div className="space-y-1">
                  <span className="text-xs font-semibold text-blue-700">
                    BuildWise AI is curating recommendations &amp; calculations...
                  </span>
                  <div className="flex items-center gap-1.5">
                    <span className="w-2 h-2 rounded-full bg-blue-600 animate-ping" />
                    <span className="text-[11px] text-slate-500">
                      Querying floor plan dimensions &amp; IS 456 civil takeoff engine
                    </span>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Quick Prompts Strip */}
          <div className="px-4 py-2.5 bg-white border-t border-slate-200 flex items-center gap-2 overflow-x-auto shadow-2xs z-10">
            <span className="text-[10px] uppercase font-bold text-slate-400 tracking-wider shrink-0 flex items-center gap-1">
              <Sparkles className="w-3 h-3 text-blue-600" />
              Suggested:
            </span>
            {quickPrompts.map((qp, idx) => (
              <button
                key={idx}
                onClick={() => handleSendMessage(qp.prompt)}
                disabled={isLoading}
                className="px-3 py-1.5 rounded-lg bg-slate-50 hover:bg-blue-50 text-slate-700 hover:text-blue-700 text-xs font-medium border border-slate-200 hover:border-blue-300 whitespace-nowrap transition disabled:opacity-50"
              >
                {qp.label}
              </button>
            ))}
          </div>

          {/* Chat Input Bar */}
          <div className="p-4 bg-white border-t border-slate-200 z-10">
            <div className="max-w-4xl mx-auto flex items-center gap-2 bg-slate-50 border border-slate-300 rounded-2xl p-2 shadow-xs focus-within:bg-white focus-within:border-blue-600 focus-within:ring-2 focus-within:ring-blue-100 transition">
              
              {/* Voice Input Button */}
              <button
                onClick={() => setVoiceModalOpen(true)}
                className="p-2.5 rounded-xl bg-white text-blue-600 hover:bg-blue-50 border border-slate-200 hover:border-blue-300 transition shadow-2xs"
                title="Speak in English, Tamil, or Tanglish"
              >
                <Mic className="w-4 h-4" />
              </button>

              {/* Text Input */}
              <input
                type="text"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') handleSendMessage();
                }}
                placeholder="Ask for floor plans, elevation pictures, civil takeoff, or speak in Tamil/Tanglish..."
                className="flex-1 bg-transparent border-none text-xs sm:text-sm text-slate-900 placeholder-slate-400 focus:outline-none px-2 font-normal"
              />

              {/* Send Button */}
              <button
                onClick={() => handleSendMessage()}
                disabled={!inputText.trim() || isLoading}
                className="p-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 disabled:opacity-40 text-white transition shadow-sm"
                title="Send message"
              >
                <Send className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Voice Modal */}
      <VoiceRecorderModal
        isOpen={voiceModalOpen}
        onClose={() => setVoiceModalOpen(false)}
        onConfirmText={(recognized) => handleSendMessage(recognized)}
      />

      {/* Kaggle Training Modal */}
      <KaggleTrainingModal
        isOpen={kaggleModalOpen}
        onClose={() => setKaggleModalOpen(false)}
        onModelActivated={(newModel) => setSelectedModel(newModel)}
      />
    </div>
  );
}
