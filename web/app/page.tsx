"use client";

import { useState, useEffect } from "react";
import { Search, Shield, TrendingUp, AlertTriangle, CheckCircle, XCircle, Mail, Loader2, Link as LinkIcon } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

export default function Home() {
  const [topic, setTopic] = useState("");
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState("");
  const [savedEmail, setSavedEmail] = useState(false);

  useEffect(() => {
    const stored = localStorage.getItem("recon_user_email");
    if (stored) {
      setEmail(stored);
      setSavedEmail(true);
    }
  }, []);

  const handleAnalyze = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!topic) return;

    if (email) {
      localStorage.setItem("recon_user_email", email);
      setSavedEmail(true);
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch("/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic, email, provider: "gemini" }),
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || "Analysis failed");
      }

      const data = await response.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getVerdictIcon = (verdict: string) => {
    switch (verdict) {
      case "GO": return <CheckCircle className="text-green-500 w-8 h-8" />;
      case "CAUTION": return <AlertTriangle className="text-yellow-500 w-8 h-8" />;
      case "NO-GO": return <XCircle className="text-red-500 w-8 h-8" />;
      default: return null;
    }
  };

  const getVerdictColor = (verdict: string) => {
    switch (verdict) {
      case "GO": return "text-green-400";
      case "CAUTION": return "text-yellow-400";
      case "NO-GO": return "text-red-400";
      default: return "";
    }
  };

  return (
    <main className="min-h-screen bg-[#0a0a0a] text-white selection:bg-cyan-500/30">
      {/* Header */}
      <nav className="border-b border-white/10 p-6">
        <div className="max-w-5xl mx-auto flex justify-between items-center">
          <div className="flex items-center gap-2">
            <Shield className="text-cyan-500 w-6 h-6" />
            <span className="font-bold text-xl tracking-tight">RECON</span>
          </div>
          <div className="hidden sm:flex items-center gap-6 text-sm text-white/60">
            <a href="https://github.com/OhYesssItsTesss/Recon" className="hover:text-white transition-colors">GitHub</a>
            <a href="#" className="hover:text-white transition-colors">Docs</a>
          </div>
        </div>
      </nav>

      <div className="max-w-3xl mx-auto px-6 py-20">
        {/* Hero */}
        <section className="text-center mb-16">
          <motion.h1 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-5xl font-extrabold mb-6 bg-gradient-to-r from-white to-white/50 bg-clip-text text-transparent"
          >
            Stop Building Ghosts.
          </motion.h1>
          <motion.p 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="text-lg text-white/60 max-w-xl mx-auto"
          >
            Recon aggregates real-world data and uses adversarial AI to tell you if your business idea is a winner or a waste of time.
          </motion.p>
        </section>

        {/* Search Box */}
        <section className="bg-white/5 border border-white/10 rounded-2xl p-8 mb-12 shadow-2xl backdrop-blur-sm">
          <form onSubmit={handleAnalyze} className="space-y-4">
            <div className="relative">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-white/30 w-5 h-5" />
              <input 
                type="text"
                placeholder="Enter your business idea (e.g., Uber for Dog Walkers)"
                className="w-full bg-black/40 border border-white/10 rounded-xl py-4 pl-12 pr-4 outline-none focus:border-cyan-500/50 transition-all text-lg"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                disabled={loading}
              />
            </div>
            
            <div className="flex flex-col sm:flex-row gap-4 items-start">
              {savedEmail ? (
                <div className="flex-1 w-full h-[54px] flex items-center px-4 bg-white/5 border border-white/10 rounded-xl">
                  <span className="text-sm text-white/50 mr-2">Using:</span>
                  <span className="text-white font-medium flex-1 truncate">{email}</span>
                  <button 
                    type="button"
                    onClick={() => { setSavedEmail(false); setEmail(""); localStorage.removeItem("recon_user_email"); }}
                    className="text-xs text-cyan-500 hover:text-cyan-400"
                  >
                    Change
                  </button>
                </div>
              ) : (
                <div className="relative flex-1 w-full">
                  <div className="relative">
                    <Mail className="absolute left-4 top-1/2 -translate-y-1/2 text-white/30 w-5 h-5" />
                    <input 
                      type="email"
                      required
                      placeholder="Enter your email to unlock report"
                      className="w-full bg-black/40 border border-white/10 rounded-xl py-3 pl-12 pr-4 outline-none focus:border-cyan-500/50 transition-all"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      disabled={loading}
                    />
                  </div>
                  <p className="text-xs text-white/30 mt-2 ml-1">🔒 No spam. I only send automations that work.</p>
                </div>
              )}
              
              <button 
                type="submit"
                className="bg-cyan-600 hover:bg-cyan-500 disabled:bg-cyan-800 disabled:cursor-not-allowed text-white font-bold py-3 px-8 rounded-xl transition-all flex items-center justify-center gap-2 w-full sm:w-auto min-w-[140px]"
                disabled={loading || !topic || !email}
              >
                {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : "Validate"}
              </button>
            </div>
          </form>
          {error && <p className="mt-4 text-red-400 text-sm">{error}</p>}
        </section>

        {/* Results */}
        <AnimatePresence>
          {result && (
            <motion.div 
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="space-y-8"
            >
              {/* Verdict Header */}
              <div className="bg-white/5 border border-white/10 rounded-2xl p-8 flex items-center justify-between">
                <div>
                  <h3 className="text-sm uppercase tracking-widest text-white/40 font-bold mb-1">Market Verdict</h3>
                  <div className="flex items-center gap-3">
                    <span className={`text-4xl font-black ${getVerdictColor(result.report.verdict)}`}>
                      {result.report.verdict}
                    </span>
                    <span className="text-2xl text-white/20 font-light">
                      ({result.report.opportunity_score}/100)
                    </span>
                  </div>
                </div>
                {getVerdictIcon(result.report.verdict)}
              </div>

              {/* Summary */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-white/5 border border-white/10 rounded-2xl p-6">
                  <h4 className="flex items-center gap-2 font-bold mb-4 text-cyan-400">
                    <TrendingUp className="w-4 h-4" /> Trend Data
                  </h4>
                  <p className="text-sm text-white/80 leading-relaxed mb-4">
                    Trajectory: <span className="font-bold">{result.trends.trajectory}</span>
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {result.trends.rising_queries.map((q: string) => (
                      <span key={q} className="bg-white/5 px-3 py-1 rounded-full text-xs text-white/60 border border-white/10">{q}</span>
                    ))}
                  </div>
                </div>

                <div className="bg-white/5 border border-white/10 rounded-2xl p-6">
                  <h4 className="flex items-center gap-2 font-bold mb-4 text-red-400">
                    <AlertTriangle className="w-4 h-4" /> Pain Points
                  </h4>
                  <ul className="space-y-2">
                    {result.report.top_pain_points.map((p: string, i: number) => (
                      <li key={i} className="text-sm text-white/70 flex gap-2">
                        <span className="text-red-500">•</span> {p}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Sources Section */}
              <div className="bg-white/5 border border-white/10 rounded-2xl p-8">
                <h4 className="flex items-center gap-2 font-bold mb-6 text-cyan-400">
                  <LinkIcon className="w-4 h-4" /> Sources Researched
                </h4>
                <div className="space-y-4">
                  {result.sources && result.sources.length > 0 ? (
                    result.sources.map((src: any, i: number) => (
                      <a 
                        key={i} 
                        href={src.url} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="block p-4 bg-black/20 border border-white/5 rounded-xl hover:border-cyan-500/30 transition-all group"
                      >
                        <div className="flex justify-between items-start gap-4">
                          <span className="text-sm font-medium text-white/80 group-hover:text-white transition-colors">{src.title}</span>
                          <LinkIcon className="w-3 h-3 text-white/20 group-hover:text-cyan-500 transition-colors flex-shrink-0 mt-1" />
                        </div>
                        <p className="text-xs text-white/30 truncate mt-1">{src.url}</p>
                      </a>
                    ))
                  ) : (
                    <p className="text-sm text-white/30 italic">No direct sources found for this topic.</p>
                  )}
                </div>
              </div>

              {/* Marketing Playbook */}
              <div className="bg-cyan-900/10 border border-cyan-500/20 rounded-2xl p-8">
                <h4 className="text-xl font-bold mb-6 text-cyan-400">The Marketing Playbook</h4>
                <div className="space-y-6">
                  <div>
                    <h5 className="text-xs uppercase tracking-tighter text-cyan-500 font-bold mb-2">Traditional</h5>
                    <p className="text-sm text-white/80">{result.report.marketing_playbook.traditional}</p>
                  </div>
                  <div className="border-t border-white/5 pt-4">
                    <h5 className="text-xs uppercase tracking-tighter text-magenta-500 font-bold mb-2">Viral / Social</h5>
                    <p className="text-sm text-white/80">{result.report.marketing_playbook.viral}</p>
                  </div>
                  <div className="border-t border-white/5 pt-4">
                    <h5 className="text-xs uppercase tracking-tighter text-green-500 font-bold mb-2">Guerrilla</h5>
                    <p className="text-sm text-white/80">{result.report.marketing_playbook.guerrilla}</p>
                  </div>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Footer */}
      <footer className="text-center py-10 border-t border-white/5 text-white/20 text-xs">
        &copy; 2026 The Architect. Built with Recon.
      </footer>
    </main>
  );
}