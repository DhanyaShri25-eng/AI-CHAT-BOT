'use client';

import React, { useState } from 'react';
import { 
  X, 
  Sparkles, 
  Copy, 
  Check, 
  ThumbsUp, 
  Palette
} from 'lucide-react';
import { RecommendedPicture } from '@/lib/types';
import { submitChatFeedback } from '@/lib/api';

interface PictureLightboxModalProps {
  picture: RecommendedPicture | null;
  onClose: () => void;
  onApplyStyle?: (style: string) => void;
}

export default function PictureLightboxModal({ picture, onClose, onApplyStyle }: PictureLightboxModalProps) {
  const [copied, setCopied] = useState(false);
  const [voted, setVoted] = useState(false);

  if (!picture) return null;

  const handleCopyPrompt = () => {
    const prompt = `Architectural 3D render, ${picture.title}, ${picture.style} aesthetic, ${picture.description}, photorealistic lighting, 8k resolution`;
    navigator.clipboard.writeText(prompt);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handlePreferStyle = async () => {
    try {
      await submitChatFeedback({
        prompt: `User prefers visual style: ${picture.title} (${picture.style})`,
        response: picture.description,
        rating: 1
      });
      setVoted(true);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm">
      <div className="relative w-full max-w-3xl overflow-hidden rounded-2xl bg-white border border-slate-200 shadow-2xl flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-3.5 border-b border-slate-200 bg-slate-50">
          <div className="flex items-center gap-2.5">
            <Palette className="w-5 h-5 text-blue-600" />
            <div>
              <h3 className="text-sm sm:text-base font-bold text-slate-900">
                {picture.title}
              </h3>
              <span className="text-[11px] text-blue-700 font-mono font-medium">
                {picture.style} • Category: {picture.category}
              </span>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Image Preview */}
        <div className="relative w-full h-80 sm:h-96 bg-slate-100 flex items-center justify-center overflow-hidden">
          <img
            src={picture.image_url}
            alt={picture.title}
            className="w-full h-full object-cover"
          />
          <div className="absolute top-3 left-3 flex flex-wrap gap-1.5">
            {picture.tags.map((tag, idx) => (
              <span
                key={idx}
                className="px-2 py-0.5 rounded-full bg-white/90 backdrop-blur text-[10px] text-blue-700 font-semibold border border-blue-200 shadow-xs"
              >
                #{tag}
              </span>
            ))}
          </div>
        </div>

        {/* Content Details */}
        <div className="p-6 space-y-4 bg-white">
          <div className="space-y-1">
            <h4 className="text-xs uppercase tracking-wider font-bold text-slate-500">
              Architectural Concept & Finishes
            </h4>
            <p className="text-xs sm:text-sm text-slate-700 leading-relaxed">
              {picture.description}
            </p>
          </div>

          {picture.specifications && (
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-2.5 pt-1">
              {Object.entries(picture.specifications).map(([key, value]) => (
                <div key={key} className="p-2.5 rounded-xl bg-slate-50 border border-slate-200">
                  <span className="text-[10px] text-slate-500 uppercase font-mono block">
                    {key.replace(/_/g, ' ')}
                  </span>
                  <span className="text-xs font-semibold text-slate-900">
                    {value}
                  </span>
                </div>
              ))}
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex flex-wrap items-center justify-between gap-3 pt-3 border-t border-slate-100">
            <div className="flex items-center gap-2">
              <button
                onClick={handlePreferStyle}
                disabled={voted}
                className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold transition flex items-center gap-1.5 border ${
                  voted
                    ? 'bg-blue-50 text-blue-700 border-blue-300 cursor-default'
                    : 'bg-white hover:bg-slate-50 text-slate-700 border-slate-300'
                }`}
              >
                <ThumbsUp className="w-3.5 h-3.5 text-blue-600" />
                {voted ? 'Preference Learned by Model (+1)' : 'Prefer this Aesthetic'}
              </button>

              <button
                onClick={handleCopyPrompt}
                className="px-3.5 py-1.5 rounded-xl bg-white hover:bg-slate-50 text-slate-700 text-xs font-medium transition flex items-center gap-1.5 border border-slate-300 shadow-2xs"
              >
                {copied ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
                {copied ? 'Prompt Copied' : 'Copy Render Prompt'}
              </button>
            </div>

            {onApplyStyle && (
              <button
                onClick={() => {
                  onApplyStyle(picture.style);
                  onClose();
                }}
                className="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold transition flex items-center gap-1.5 shadow-xs"
              >
                <Sparkles className="w-3.5 h-3.5" />
                Apply Style to Design Studio
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
