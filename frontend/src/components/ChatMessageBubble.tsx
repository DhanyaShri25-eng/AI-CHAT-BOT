'use client';

import React, { useState } from 'react';
import { 
  Bot, 
  User, 
  Copy, 
  Check, 
  Volume2, 
  VolumeX, 
  ThumbsUp, 
  ThumbsDown, 
  Layers, 
  Calculator, 
  Palette, 
  Brain,
  Eye
} from 'lucide-react';
import { ChatMessage, RecommendedPicture } from '@/lib/types';
import { submitChatFeedback } from '@/lib/api';
import PictureLightboxModal from './PictureLightboxModal';
import Link from 'next/link';

interface ChatMessageBubbleProps {
  message: ChatMessage;
  onRegenerate?: () => void;
  onApplyStyle?: (style: string) => void;
}

export default function ChatMessageBubble({ message, onRegenerate, onApplyStyle }: ChatMessageBubbleProps) {
  const [copied, setCopied] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [feedback, setFeedback] = useState<number | null>(null);
  const [feedbackMessage, setFeedbackMessage] = useState<string | null>(null);
  const [selectedPicture, setSelectedPicture] = useState<RecommendedPicture | null>(null);

  const isAssistant = message.sender === 'assistant';

  const handleCopy = () => {
    navigator.clipboard.writeText(message.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleSpeak = () => {
    if ('speechSynthesis' in window) {
      if (isSpeaking) {
        window.speechSynthesis.cancel();
        setIsSpeaking(false);
      } else {
        const cleanText = message.content.replace(/[#*`|]/g, '');
        const utterance = new SpeechSynthesisUtterance(cleanText);
        utterance.rate = 1.0;
        utterance.onend = () => setIsSpeaking(false);
        utterance.onerror = () => setIsSpeaking(false);
        setIsSpeaking(true);
        window.speechSynthesis.speak(utterance);
      }
    }
  };

  const handleFeedback = async (score: number) => {
    setFeedback(score);
    setFeedbackMessage(score > 0 ? 'Feedback recorded!' : 'Penalty aligned');
    try {
      await submitChatFeedback({
        prompt: 'User chat query',
        response: message.content,
        rating: score
      });
    } catch (e) {
      // optimistic update
    }
    setTimeout(() => setFeedbackMessage(null), 3000);
  };

  // Render markdown-like bullet points and bold lines
  const renderFormattedContent = (content: string) => {
    const lines = content.split('\n');

    return (
      <div className="space-y-1.5 text-xs sm:text-sm leading-relaxed">
        {lines.map((line, idx) => {
          if (line.startsWith('### ')) {
            return (
              <h4 key={idx} className={`text-sm font-bold pt-2 pb-1 border-b ${isAssistant ? 'text-blue-800 border-blue-100' : 'text-white border-white/20'}`}>
                {line.replace('### ', '')}
              </h4>
            );
          }
          if (line.startsWith('## ')) {
            return (
              <h3 key={idx} className={`text-base font-bold pt-2 ${isAssistant ? 'text-slate-900' : 'text-white'}`}>
                {line.replace('## ', '')}
              </h3>
            );
          }
          if (line.startsWith('- ')) {
            return (
              <div key={idx} className="flex items-start gap-2 pl-2">
                <span className={`font-bold ${isAssistant ? 'text-blue-600' : 'text-white'}`}>•</span>
                <span dangerouslySetInnerHTML={{ __html: formatInline(line.substring(2)) }} />
              </div>
            );
          }
          if (line.startsWith('|') && line.includes('|')) {
            // Table row preview
            return (
              <div key={idx} className={`font-mono text-[11px] px-2 py-1 rounded overflow-x-auto whitespace-pre border ${
                isAssistant ? 'bg-slate-50 border-slate-200 text-slate-800' : 'bg-blue-700/60 border-blue-500/40 text-blue-50'
              }`}>
                {line}
              </div>
            );
          }
          if (!line.trim()) {
            return <div key={idx} className="h-1" />;
          }
          return (
            <p key={idx} dangerouslySetInnerHTML={{ __html: formatInline(line) }} />
          );
        })}
      </div>
    );
  };

  const formatInline = (str: string) => {
    if (isAssistant) {
      return str
        .replace(/\*\*(.*?)\*\*/g, '<strong class="text-slate-900 font-bold">$1</strong>')
        .replace(/\*(.*?)\*/g, '<em class="text-blue-700 font-medium">$1</em>');
    }
    return str
      .replace(/\*\*(.*?)\*\*/g, '<strong class="text-white font-bold">$1</strong>')
      .replace(/\*(.*?)\*/g, '<em class="text-blue-100">$1</em>');
  };

  return (
    <>
      <div
        className={`flex gap-3 max-w-4xl mx-auto py-4 px-4 sm:px-6 rounded-2xl transition ${
          isAssistant
            ? 'bg-white border border-slate-200 shadow-sm text-slate-800'
            : 'bg-blue-600 text-white shadow-md ml-auto'
        }`}
      >
        {/* Avatar */}
        <div className="shrink-0">
          {isAssistant ? (
            <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-blue-600 to-indigo-600 flex items-center justify-center text-white shadow-sm">
              <Bot className="w-4 h-4" />
            </div>
          ) : (
            <div className="w-8 h-8 rounded-xl bg-blue-700 flex items-center justify-center text-white">
              <User className="w-4 h-4" />
            </div>
          )}
        </div>

        {/* Message Content */}
        <div className="flex-1 space-y-3 min-w-0">
          <div className="flex items-center justify-between">
            <span className={`text-xs font-semibold ${isAssistant ? 'text-slate-700' : 'text-blue-100'}`}>
              {isAssistant ? 'BuildWise AI Consultant' : 'You'}
            </span>
            {message.model_used && (
              <span className={`text-[10px] font-mono px-2 py-0.5 rounded border flex items-center gap-1 ${
                isAssistant ? 'text-blue-700 bg-blue-50 border-blue-200' : 'text-blue-100 bg-blue-700/60 border-blue-400'
              }`}>
                <Brain className="w-2.5 h-2.5" />
                {message.model_used}
              </span>
            )}
          </div>

          {/* Text */}
          <div className={isAssistant ? 'text-slate-700' : 'text-white'}>
            {renderFormattedContent(message.content)}
          </div>

          {/* In-Context Continuous Learning Insight Badge */}
          {message.structured_data?.training_insight && (
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-blue-50 border border-blue-200 text-[11px] text-blue-800">
              <Brain className="w-3.5 h-3.5 text-blue-600 shrink-0" />
              <span>
                <strong>Model Memory Adapted:</strong> Style: <em>{message.structured_data.training_insight.user_style_memory || 'Modern'}</em> • Turn logged into active SFT / DPO training buffer
              </span>
            </div>
          )}

          {/* Recommended Pictures Visual Showcase */}
          {message.structured_data?.recommended_pictures && message.structured_data.recommended_pictures.length > 0 && (
            <div className="pt-2 space-y-2">
              <div className="flex items-center justify-between text-xs font-bold text-blue-800 border-b border-blue-100 pb-1">
                <span className="flex items-center gap-1.5">
                  <Palette className="w-4 h-4 text-blue-600" />
                  Recommended Architectural Pictures & Concepts
                </span>
                <span className="text-[10px] font-mono text-slate-500">
                  {message.structured_data.recommended_pictures.length} concepts curated
                </span>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                {message.structured_data.recommended_pictures.map((pic) => (
                  <div
                    key={pic.id}
                    onClick={() => setSelectedPicture(pic)}
                    className="group cursor-pointer rounded-xl overflow-hidden bg-white border border-slate-200 hover:border-blue-400 transition-all duration-300 flex flex-col shadow-xs hover:shadow-md"
                  >
                    <div className="relative h-32 w-full overflow-hidden bg-slate-100">
                      <img
                        src={pic.thumbnail_url || pic.image_url}
                        alt={pic.title}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                      />
                      <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-60" />
                      <div className="absolute top-2 left-2 px-2 py-0.5 rounded bg-white/90 backdrop-blur text-[9px] font-semibold text-blue-700 border border-blue-100 shadow-xs">
                        {pic.style}
                      </div>
                      <div className="absolute bottom-2 right-2 p-1.5 rounded-md bg-white text-blue-600 opacity-0 group-hover:opacity-100 transition shadow-sm">
                        <Eye className="w-3.5 h-3.5" />
                      </div>
                    </div>
                    <div className="p-2.5 flex-1 flex flex-col justify-between space-y-1">
                      <h5 className="text-xs font-bold text-slate-800 group-hover:text-blue-600 transition line-clamp-1">
                        {pic.title}
                      </h5>
                      <p className="text-[11px] text-slate-500 line-clamp-2 leading-tight">
                        {pic.description}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Embedded Dynamic Interactive Cards */}
          {message.structured_data && (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
              {message.structured_data.floor_plan && (
                <div className="p-3 rounded-xl bg-blue-50 border border-blue-200 flex items-center justify-between">
                  <div className="flex items-center gap-2.5">
                    <Layers className="w-5 h-5 text-blue-600" />
                    <div>
                      <span className="text-xs font-bold text-slate-900 block">
                        {message.structured_data.floor_plan.title}
                      </span>
                      <span className="text-[11px] text-slate-600">
                        {message.structured_data.floor_plan.total_area_sqft} sq.ft • {message.structured_data.floor_plan.rooms.length} Rooms
                      </span>
                    </div>
                  </div>
                  <Link
                    href="/studio"
                    className="px-3 py-1 rounded-lg bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold transition shadow-xs"
                  >
                    Open Studio
                  </Link>
                </div>
              )}

              {message.structured_data.cost_estimate && (
                <div className="p-3 rounded-xl bg-emerald-50 border border-emerald-200 flex items-center justify-between">
                  <div className="flex items-center gap-2.5">
                    <Calculator className="w-5 h-5 text-emerald-600" />
                    <div>
                      <span className="text-xs font-bold text-slate-900 block">
                        ₹{message.structured_data.cost_estimate.total_expected.toLocaleString()}
                      </span>
                      <span className="text-[11px] text-slate-600">
                        ₹{Math.round(message.structured_data.cost_estimate.rate_per_sqft)} / sq.ft • Itemized Estimate
                      </span>
                    </div>
                  </div>
                  <Link
                    href="/estimation"
                    className="px-3 py-1 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold transition shadow-xs"
                  >
                    View Details
                  </Link>
                </div>
              )}
            </div>
          )}

          {/* Action Buttons for AI message */}
          {isAssistant && (
            <div className="flex items-center gap-2 pt-2 border-t border-slate-100">
              <button
                onClick={handleCopy}
                className="p-1.5 rounded-lg text-slate-500 hover:text-slate-800 hover:bg-slate-100 transition text-xs flex items-center gap-1"
                title="Copy message"
              >
                {copied ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
                <span className="text-[10px] font-medium">{copied ? 'Copied' : 'Copy'}</span>
              </button>

              <button
                onClick={handleSpeak}
                className={`p-1.5 rounded-lg transition text-xs flex items-center gap-1 ${
                  isSpeaking ? 'text-blue-600 bg-blue-50 font-medium' : 'text-slate-500 hover:text-slate-800 hover:bg-slate-100'
                }`}
                title="Text-to-speech audio"
              >
                {isSpeaking ? <VolumeX className="w-3.5 h-3.5 animate-pulse" /> : <Volume2 className="w-3.5 h-3.5" />}
                <span className="text-[10px] font-medium">{isSpeaking ? 'Mute' : 'Listen'}</span>
              </button>

              <div className="h-3 w-px bg-slate-200 mx-1" />

              <button
                onClick={() => handleFeedback(1)}
                className={`p-1.5 rounded-lg transition flex items-center gap-1 ${
                  feedback === 1 ? 'text-blue-700 bg-blue-50 border border-blue-200 font-semibold' : 'text-slate-500 hover:text-slate-800 hover:bg-slate-100'
                }`}
                title="Good response (Train model +1)"
              >
                <ThumbsUp className="w-3.5 h-3.5" />
                <span className="text-[10px] font-medium">Train +1</span>
              </button>

              <button
                onClick={() => handleFeedback(-1)}
                className={`p-1.5 rounded-lg transition flex items-center gap-1 ${
                  feedback === -1 ? 'text-rose-700 bg-rose-50 border border-rose-200 font-semibold' : 'text-slate-500 hover:text-slate-800 hover:bg-slate-100'
                }`}
                title="Poor response (DPO alignment penalty)"
              >
                <ThumbsDown className="w-3.5 h-3.5" />
                <span className="text-[10px] font-medium">Align -1</span>
              </button>

              {feedbackMessage && (
                <span className="text-[10px] text-emerald-600 font-semibold ml-2">
                  ✓ {feedbackMessage}
                </span>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Picture Lightbox Modal */}
      <PictureLightboxModal
        picture={selectedPicture}
        onClose={() => setSelectedPicture(null)}
        onApplyStyle={onApplyStyle}
      />
    </>
  );
}
