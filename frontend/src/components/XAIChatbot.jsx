import React, { useState, useRef, useEffect } from 'react';
import { MessageCircle, X, Send, Bot, User, ChevronDown, Sparkles } from 'lucide-react';
import axios from 'axios';
import { API_URL, ENDPOINTS } from '../config/api';

const XAIChatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      role: 'bot',
      text: "Hello! 🌱 I'm your **SmartCropX AI Assistant**. Ask me about crops, diseases, soil types, market prices, or how our AI explanations (Grad-CAM & SHAP) work!",
      suggestions: ["What crops do you support?", "Explain Grad-CAM", "Soil tips", "Farming advice"],
    },
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [showPulse, setShowPulse] = useState(true);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  useEffect(() => {
    if (isOpen) {
      setShowPulse(false);
      setTimeout(() => inputRef.current?.focus(), 300);
    }
  }, [isOpen]);

  const sendMessage = async (text) => {
    if (!text.trim()) return;

    const userMsg = { role: 'user', text: text.trim() };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setIsTyping(true);

    try {
      const res = await axios.post(ENDPOINTS.CHAT, { message: text.trim() }, { timeout: 10000 });
      const data = res.data;
      const modeLabel = data.mode === 'fallback' ? ' _(demo mode)_' : '';
      setMessages((prev) => [
        ...prev,
        {
          role: 'bot',
          text: (data.reply || "I'm not sure how to answer that.") + modeLabel,
          suggestions: data.suggestions || [],
        },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: 'bot',
          text: "Sorry, I couldn't connect to the server. Please make sure the backend is running and try again!",
          suggestions: ["Help", "Try again"],
        },
      ]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage(input);
    }
  };

  /* ── Simple markdown bold + newline renderer ── */
  const renderMarkdown = (text) => {
    const parts = text.split(/(\*\*[^*]+\*\*|\n)/g);
    return parts.map((part, i) => {
      if (part === '\n') return <br key={i} />;
      if (part.startsWith('**') && part.endsWith('**'))
        return (
          <strong key={i} className="font-semibold text-green-300">
            {part.slice(2, -2)}
          </strong>
        );
      return <span key={i}>{part}</span>;
    });
  };

  return (
    <>
      {/* ── Floating button ── */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="fixed bottom-6 right-6 z-50 bg-gradient-to-br from-green-500 to-emerald-600 text-white rounded-full w-16 h-16 flex items-center justify-center shadow-2xl hover:scale-110 transition-all duration-300 group"
          aria-label="Open AI Chat"
        >
          <MessageCircle size={28} className="group-hover:rotate-12 transition-transform" />
          {showPulse && (
            <>
              <span className="absolute inset-0 rounded-full bg-green-400 animate-ping opacity-30" />
              <span className="absolute -top-1 -right-1 bg-yellow-400 text-[10px] text-black font-bold rounded-full w-5 h-5 flex items-center justify-center">
                AI
              </span>
            </>
          )}
        </button>
      )}

      {/* ── Chat window ── */}
      {isOpen && (
        <div className="fixed bottom-6 right-6 z-50 w-[380px] max-w-[calc(100vw-2rem)] h-[560px] max-h-[calc(100vh-3rem)] bg-gray-900 rounded-2xl shadow-2xl border border-gray-700 flex flex-col overflow-hidden animate-slideUp">
          {/* Header */}
          <div className="bg-gradient-to-r from-green-600 to-emerald-700 px-4 py-3 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="bg-white/20 rounded-lg p-1.5">
                <Sparkles size={18} className="text-yellow-300" />
              </div>
              <div>
                <h3 className="text-white font-bold text-sm leading-tight">SmartCropX AI</h3>
                <p className="text-green-200 text-[11px]">Explainable AI Assistant</p>
              </div>
            </div>
            <div className="flex items-center gap-1">
              <button
                onClick={() => setIsOpen(false)}
                className="text-white/70 hover:text-white hover:bg-white/10 rounded-lg p-1.5 transition-colors"
                aria-label="Minimize chat"
              >
                <ChevronDown size={18} />
              </button>
              <button
                onClick={() => setIsOpen(false)}
                className="text-white/70 hover:text-white hover:bg-white/10 rounded-lg p-1.5 transition-colors"
                aria-label="Close chat"
              >
                <X size={18} />
              </button>
            </div>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto px-3 py-3 space-y-3 scrollbar-thin scrollbar-thumb-gray-700">
            {messages.map((msg, idx) => (
              <div key={idx}>
                <div className={`flex items-start gap-2 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
                  {/* Avatar */}
                  <div
                    className={`flex-shrink-0 w-7 h-7 rounded-full flex items-center justify-center ${
                      msg.role === 'bot'
                        ? 'bg-gradient-to-br from-green-500 to-emerald-600'
                        : 'bg-gradient-to-br from-blue-500 to-indigo-600'
                    }`}
                  >
                    {msg.role === 'bot' ? <Bot size={14} className="text-white" /> : <User size={14} className="text-white" />}
                  </div>

                  {/* Bubble */}
                  <div
                    className={`max-w-[80%] rounded-xl px-3 py-2 text-sm leading-relaxed ${
                      msg.role === 'bot'
                        ? 'bg-gray-800 text-gray-200 rounded-tl-sm'
                        : 'bg-green-600 text-white rounded-tr-sm'
                    }`}
                  >
                    {renderMarkdown(msg.text)}
                  </div>
                </div>

                {/* Suggestions */}
                {msg.role === 'bot' && msg.suggestions?.length > 0 && idx === messages.length - 1 && (
                  <div className="flex flex-wrap gap-1.5 mt-2 ml-9">
                    {msg.suggestions.map((s, i) => (
                      <button
                        key={i}
                        onClick={() => sendMessage(s)}
                        className="text-[11px] bg-gray-800 hover:bg-green-700 text-green-300 hover:text-white border border-gray-700 hover:border-green-600 rounded-full px-3 py-1 transition-all duration-200"
                      >
                        {s}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            ))}

            {/* Typing indicator */}
            {isTyping && (
              <div className="flex items-start gap-2">
                <div className="w-7 h-7 rounded-full bg-gradient-to-br from-green-500 to-emerald-600 flex items-center justify-center flex-shrink-0">
                  <Bot size={14} className="text-white" />
                </div>
                <div className="bg-gray-800 rounded-xl rounded-tl-sm px-4 py-2">
                  <div className="flex gap-1">
                    <span className="w-2 h-2 bg-green-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                    <span className="w-2 h-2 bg-green-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                    <span className="w-2 h-2 bg-green-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="border-t border-gray-700 px-3 py-2 bg-gray-800/50">
            <div className="flex items-center gap-2">
              <input
                ref={inputRef}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask about crops, diseases, XAI…"
                className="flex-1 bg-gray-800 text-white text-sm rounded-lg px-3 py-2 outline-none focus:ring-2 focus:ring-green-500 border border-gray-700 placeholder-gray-500"
                disabled={isTyping}
              />
              <button
                onClick={() => sendMessage(input)}
                disabled={!input.trim() || isTyping}
                className="bg-green-600 hover:bg-green-500 disabled:bg-gray-700 disabled:text-gray-500 text-white rounded-lg p-2 transition-colors"
                aria-label="Send message"
              >
                <Send size={16} />
              </button>
            </div>
            <p className="text-[10px] text-gray-500 mt-1 text-center">
              Powered by SmartCropX Explainable AI
            </p>
          </div>
        </div>
      )}

      {/* Slide-up animation */}
      <style>{`
        @keyframes slideUp {
          from { opacity: 0; transform: translateY(20px) scale(0.95); }
          to   { opacity: 1; transform: translateY(0) scale(1); }
        }
        .animate-slideUp { animation: slideUp 0.3s ease-out; }
      `}</style>
    </>
  );
};

export default XAIChatbot;
