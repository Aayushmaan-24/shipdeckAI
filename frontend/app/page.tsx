"use client";

import { useState, useRef, useEffect } from "react";
import { Hero } from "@/components/Hero";
import { Features } from "@/components/Features";
import { Workflow } from "@/components/Workflow";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Progress } from "@/components/ui/progress";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import {
  Github,
  Sparkles,
  Download,
  Loader2,
  CheckCircle2,
  AlertCircle,
  Terminal
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Slide,
  Status,
  extractMessages,
  extractDeckStructure
} from "@/lib/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export default function Home() {
  const [githubUrl, setGithubUrl] = useState("");
  const [status, setStatus] = useState<Status>("idle");
  const [progress, setProgress] = useState<string[]>([]);
  const [slides, setSlides] = useState<Slide[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [isDownloading, setIsDownloading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [progress]);

  async function handleDownload() {
    if (slides.length === 0) return;
    setIsDownloading(true);
    try {
      const response = await fetch(`${API_URL}/api/download`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ slides }),
      });

      if (!response.ok) throw new Error("Download failed");

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "pitch_deck.pptx";
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      console.error("Download error:", err);
      setError("Failed to download PowerPoint file.");
    } finally {
      setIsDownloading(false);
    }
  }

  async function handleGenerate() {
    const url = githubUrl.trim();
    if (!url) {
      setError("Please enter a GitHub repository URL.");
      return;
    }

    setStatus("generating");
    setProgress([]);
    setSlides([]);
    setError(null);

    try {
      const response = await fetch(`${API_URL}/api/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ github_url: url }),
      });

      if (!response.ok) {
        throw new Error(`Request failed (${response.status})`);
      }

      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error("No response stream available");
      }

      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const parts = buffer.split("\n\n");
        buffer = parts.pop() ?? "";

        for (const part of parts) {
          const line = part.trim();
          if (!line.startsWith("data: ")) continue;

          let payload: Record<string, unknown>;
          try {
            payload = JSON.parse(line.slice(6)) as Record<string, unknown>;
          } catch (e) {
            console.error("Failed to parse SSE payload:", e);
            continue;
          }

          if ("error" in payload && typeof payload.error === "string") {
            throw new Error(payload.error);
          }

          const newMessages = extractMessages(payload);
          if (newMessages.length > 0) {
            setProgress((prev) => [...prev, ...newMessages]);
          }

          const deck = extractDeckStructure(payload);
          if (deck) {
            setSlides(deck);
          }
        }
      }

      setStatus("done");
    } catch (err) {
      setStatus("error");
      setError(err instanceof Error ? err.message : "Generation failed");
    }
  }

  const isGenerating = status === "generating";

  return (
    <div className="min-h-screen bg-slate-950 text-white selection:bg-blue-500/30">
      <nav className="fixed top-0 w-full z-50 border-b border-white/5 bg-slate-950/80 backdrop-blur-md">
        <div className="container mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <Sparkles className="h-5 w-5 text-white" />
            </div>
            <span className="text-xl font-bold tracking-tight">ShipDeck</span>
          </div>
          <div className="hidden md:flex items-center gap-8 text-sm font-medium text-slate-400">
            <a href="#" className="hover:text-white transition-colors">How it works</a>
            <a href="#" className="hover:text-white transition-colors">Features</a>
            <a href="#" className="hover:text-white transition-colors">Showcase</a>
          </div>
          <Button variant="ghost" size="sm" className="hidden sm:flex text-slate-400 hover:text-white">
            <Github className="mr-2 h-4 w-4" /> v1.0
          </Button>
        </div>
      </nav>

      <main>
        <Hero />

        <section id="generator" className="container mx-auto px-6 py-12">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
          >
            <Card className="max-w-4xl mx-auto border-slate-800 bg-slate-900/40 backdrop-blur-sm overflow-hidden shadow-2xl">
              <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-blue-600 to-indigo-600" />
              <CardHeader className="pt-8 pb-4">
                <CardTitle className="text-2xl font-bold flex items-center gap-2">
                   Launch your project analysis
                </CardTitle>
                <p className="text-slate-400 text-sm">Paste your GitHub repository URL to start the multi-agent generation process.</p>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="flex flex-col sm:flex-row gap-3">
                  <div className="relative flex-1">
                    <Github className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-slate-500" />
                    <Input
                      type="url"
                      placeholder="https://github.com/owner/repo"
                      value={githubUrl}
                      onChange={(e) => setGithubUrl(e.target.value)}
                      disabled={isGenerating}
                      className="pl-10 h-12 bg-slate-950 border-slate-800 focus-visible:ring-blue-600 text-base"
                    />
                  </div>
                  <Button
                    onClick={handleGenerate}
                    disabled={isGenerating || !githubUrl}
                    className="h-12 px-8 bg-blue-600 hover:bg-blue-500 font-bold"
                  >
                    {isGenerating ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        Generating
                      </>
                    ) : (
                      "Analyze & Build Deck"
                    )}
                  </Button>
                </div>

                <AnimatePresence>
                  {error && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: "auto" }}
                      exit={{ opacity: 0, height: 0 }}
                      className="rounded-lg border border-red-500/20 bg-red-500/10 p-4 text-red-400 flex items-center gap-3"
                    >
                      <AlertCircle className="h-5 w-5 shrink-0" />
                      <span className="text-sm">{error}</span>
                    </motion.div>
                  )}
                </AnimatePresence>

                {isGenerating && (
                  <div className="space-y-3">
                    <div className="flex justify-between text-sm text-slate-400">
                      <span>Orchestrating agents...</span>
                      <span>This usually takes 30-60 seconds</span>
                    </div>
                    <Progress value={progress.length * 10} className="h-1.5" />
                  </div>
                )}

                <AnimatePresence>
                  {progress.length > 0 && (
                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="space-y-3"
                    >
                      <div className="flex items-center gap-2 text-sm font-semibold text-slate-300">
                        <Terminal className="h-4 w-4" /> Agent Execution Log
                      </div>
                      <div
                        ref={scrollRef}
                        className="rounded-lg bg-slate-950 border border-slate-800 p-4 font-mono text-[13px] text-slate-300 h-40 overflow-y-auto space-y-2"
                      >
                        {progress.map((line, i) => (
                          <div key={i} className="flex gap-2">
                            <span className="text-blue-500/50 shrink-0 select-none">[{i+1}]</span>
                            <span className="flex-1">{line}</span>
                          </div>
                        ))}
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </CardContent>
            </Card>
          </motion.div>
        </section>

        <AnimatePresence>
          {slides.length > 0 && (
            <motion.section
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="container mx-auto px-6 py-12"
            >
              <div className="flex flex-col sm:flex-row items-center justify-between mb-8 gap-4">
                <div>
                  <h2 className="text-2xl font-bold flex items-center gap-3">
                    <CheckCircle2 className="h-6 w-6 text-emerald-500" />
                    Preview Deck Structure
                  </h2>
                  <p className="text-slate-400">Successfully generated {slides.length} professional slides.</p>
                </div>
                <Button
                  onClick={handleDownload}
                  disabled={isDownloading}
                  size="lg"
                  className="bg-emerald-600 hover:bg-emerald-500 text-white font-bold px-8 shadow-xl shadow-emerald-600/20"
                >
                  {isDownloading ? (
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  ) : (
                    <Download className="mr-2 h-5 w-5" />
                  )}
                  Download Pitch Deck (PPTX)
                </Button>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {slides.map((slide, idx) => (
                  <motion.div
                    key={idx}
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: idx * 0.05 }}
                  >
                    <Card className="aspect-video bg-slate-900 border-slate-800 overflow-hidden group cursor-default shadow-lg">
                      <div className="h-1 w-full bg-blue-600 opacity-50 group-hover:opacity-100 transition-opacity" />
                      <CardContent className="p-4 flex flex-col h-full">
                        <div className="flex items-center justify-between mb-2">
                           <span className="text-[10px] uppercase tracking-widest text-slate-500 font-bold">Slide {slide.slide}</span>
                           <span className="text-[10px] text-slate-600">ShipDeck v1.0</span>
                        </div>
                        <h3 className="text-sm font-bold text-white mb-2 line-clamp-1 border-b border-white/5 pb-2">
                          {slide.title}
                        </h3>
                        <p className="flex-1 text-[11px] text-slate-400 whitespace-pre-wrap overflow-hidden line-clamp-[6]">
                          {slide.content}
                        </p>
                      </CardContent>
                    </Card>
                  </motion.div>
                ))}
              </div>
            </motion.section>
          )}
        </AnimatePresence>

        <Features />
        <Workflow />
      </main>

      <footer className="py-12 border-t border-white/5 bg-slate-950">
        <div className="container mx-auto px-6 flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 bg-blue-600 rounded flex items-center justify-center">
              <Sparkles className="h-3 w-3 text-white" />
            </div>
            <span className="font-bold">ShipDeck</span>
          </div>
          <p className="text-slate-500 text-sm">© 2026 ShipDeck AI. Built for the modern builder.</p>
          <div className="flex items-center gap-6 text-sm text-slate-400">
            <a href="#" className="hover:text-white">Privacy</a>
            <a href="#" className="hover:text-white">Terms</a>
            <a href="https://github.com" className="hover:text-white flex items-center gap-1">
              <Github className="h-4 w-4" /> GitHub
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
