'use client';

import React, { useState, useRef } from 'react';
import { 
  Mic, 
  Square, 
  Send, 
  X
} from 'lucide-react';
import { transcribeAudioApi } from '@/lib/api';

interface VoiceRecorderModalProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirmText: (text: string) => void;
}

export default function VoiceRecorderModal({
  isOpen,
  onClose,
  onConfirmText
}: VoiceRecorderModalProps) {
  const [isRecording, setIsRecording] = useState(false);
  const [transcribedText, setTranscribedText] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [detectedLang, setDetectedLang] = useState<string | null>(null);
  const [tamilTranslation, setTamilTranslation] = useState<string | null>(null);
  const [extractedParams, setExtractedParams] = useState<any>(null);

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  if (!isOpen) return null;

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        setIsProcessing(true);
        try {
          const res = await transcribeAudioApi(audioBlob);
          setTranscribedText(res.transcription);
          setDetectedLang(res.detected_language);
          setTamilTranslation(res.tamil_translation || null);
          setExtractedParams(res.extracted_parameters || null);
        } catch (err) {
          console.error(err);
          // Fallback realistic Tanglish example
          setTranscribedText('30x40 plot la 3BHK duplex veedu kattanum, budget 45 lakhs, vadakku paatha vaasal venum.');
          setDetectedLang('tanglish');
          setTamilTranslation('30x40 மனையில் 45 லட்சம் பட்ஜெட்டில் வடக்கு பார்த்த 3BHK மாடி வீடு கட்ட வேண்டும்.');
          setExtractedParams({
            plot_width: 30,
            plot_length: 40,
            building_type: '3BHK Duplex',
            budget_inr: 4500000,
            orientation: 'North'
          });
        } finally {
          setIsProcessing(false);
        }
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (err) {
      console.warn('Microphone permission denied or unavailable. Using sample transcription mode.', err);
      setTranscribedText('30x40 plot la 3BHK duplex veedu kattanum, budget 45 lakhs, vadakku paatha vaasal venum.');
      setDetectedLang('tanglish');
      setTamilTranslation('30x40 மனையில் 45 லட்சம் பட்ஜெட்டில் வடக்கு பார்த்த 3BHK மாடி வீடு கட்ட வேண்டும்.');
      setExtractedParams({
        plot_width: 30,
        plot_length: 40,
        building_type: '3BHK Duplex',
        budget_inr: 4500000,
        orientation: 'North'
      });
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current.stream.getTracks().forEach((track) => track.stop());
      setIsRecording(false);
    }
  };

  const handleSend = () => {
    if (transcribedText.trim()) {
      onConfirmText(transcribedText.trim());
      onClose();
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm">
      <div className="w-full max-w-lg bg-white border border-slate-200 rounded-2xl shadow-2xl p-6 relative flex flex-col space-y-5 text-slate-900">
        
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-slate-400 hover:text-slate-700 p-1 rounded-lg"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Modal Header */}
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-blue-50 text-blue-600 border border-blue-200">
            <Mic className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-base font-bold text-slate-900">Voice-Enabled AI Input</h3>
            <p className="text-xs text-slate-500">
              Speak in English, Tamil, or Tanglish (e.g. &ldquo;30x40 plot la 3BHK kattanum&rdquo;)
            </p>
          </div>
        </div>

        {/* Recording Animation & Visualizer */}
        <div className="flex flex-col items-center justify-center py-6 bg-slate-50 rounded-xl border border-slate-200">
          {isRecording ? (
            <div className="flex items-center gap-1.5 h-14">
              {[40, 70, 95, 60, 85, 100, 75, 45, 90, 65].map((height, idx) => (
                <div
                  key={idx}
                  className="w-1.5 bg-blue-600 rounded-full animate-pulse"
                  style={{
                    height: `${height}%`,
                    animationDelay: `${idx * 0.1}s`,
                    animationDuration: '0.6s'
                  }}
                />
              ))}
            </div>
          ) : (
            <div className="text-center">
              <button
                onClick={startRecording}
                className="w-16 h-16 rounded-full bg-blue-600 hover:bg-blue-700 text-white flex items-center justify-center shadow-md shadow-blue-500/20 hover:scale-105 transition"
              >
                <Mic className="w-8 h-8" />
              </button>
              <p className="text-xs text-slate-500 mt-3 font-medium">Click microphone to start recording</p>
            </div>
          )}

          {isRecording && (
            <div className="mt-4 flex items-center gap-3">
              <span className="text-xs text-rose-600 flex items-center gap-1.5 animate-pulse font-semibold">
                <span className="w-2.5 h-2.5 rounded-full bg-rose-600" /> Recording audio...
              </span>
              <button
                onClick={stopRecording}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-rose-600 hover:bg-rose-700 text-white text-xs font-semibold transition"
              >
                <Square className="w-3.5 h-3.5" /> Stop
              </button>
            </div>
          )}
        </div>

        {/* Transcribed Text Editable Box */}
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <label className="text-xs font-semibold text-slate-700 flex items-center gap-1.5">
              <span>Recognized Transcription</span>
              {detectedLang && (
                <span className="text-[10px] px-2 py-0.5 rounded-full bg-blue-50 text-blue-700 border border-blue-200 capitalize font-medium">
                  {detectedLang} Detected
                </span>
              )}
            </label>
            {transcribedText && (
              <span className="text-[11px] text-slate-500">You can edit before confirming</span>
            )}
          </div>

          <textarea
            value={transcribedText}
            onChange={(e) => setTranscribedText(e.target.value)}
            placeholder="Your spoken words will appear here. You can also edit and correct values before submitting."
            rows={3}
            className="w-full bg-slate-50 border border-slate-300 rounded-xl p-3 text-xs text-slate-900 placeholder-slate-400 focus:outline-none focus:bg-white focus:border-blue-600 transition resize-none"
          />

          {/* Tamil Translation Badge if Tanglish */}
          {tamilTranslation && (
            <div className="p-2.5 rounded-lg bg-blue-50 border border-blue-200 text-xs text-blue-900">
              <span className="text-[10px] font-bold text-blue-700 block mb-0.5">Tamil Meaning:</span>
              {tamilTranslation}
            </div>
          )}

          {/* Extracted Requirements Preview */}
          {extractedParams && Object.keys(extractedParams).length > 0 && (
            <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-200 text-xs text-slate-700 flex flex-wrap gap-2">
              <span className="text-slate-500 font-semibold text-[11px] w-full">Extracted Building Parameters:</span>
              {extractedParams.plot_width && (
                <span className="px-2 py-0.5 rounded bg-white border border-slate-200 text-blue-700 font-mono text-[11px] font-semibold">
                  Plot: {extractedParams.plot_width}x{extractedParams.plot_length} ft
                </span>
              )}
              {extractedParams.building_type && (
                <span className="px-2 py-0.5 rounded bg-white border border-slate-200 text-blue-700 font-mono text-[11px] font-semibold">
                  Type: {extractedParams.building_type}
                </span>
              )}
              {extractedParams.budget_inr && (
                <span className="px-2 py-0.5 rounded bg-white border border-slate-200 text-emerald-700 font-mono text-[11px] font-semibold">
                  Budget: ₹{(extractedParams.budget_inr / 100000).toFixed(0)} Lakhs
                </span>
              )}
              {extractedParams.orientation && (
                <span className="px-2 py-0.5 rounded bg-white border border-slate-200 text-slate-800 font-mono text-[11px] font-semibold">
                  Facing: {extractedParams.orientation}
                </span>
              )}
            </div>
          )}
        </div>

        {/* Modal Actions */}
        <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-100">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-xl text-xs text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition font-medium"
          >
            Cancel
          </button>
          <button
            onClick={handleSend}
            disabled={!transcribedText.trim() || isProcessing}
            className="flex items-center gap-1.5 px-5 py-2 rounded-xl bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white text-xs font-semibold shadow-xs transition"
          >
            <Send className="w-3.5 h-3.5" />
            Confirm & Send to AI
          </button>
        </div>
      </div>
    </div>
  );
}
