"use client";

import { useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

type Slide = {
  slide: number;
  title: string;
  content: string;
};

type Status = "idle" | "generating" | "done" | "error";

function extractMessages(event: Record<string, unknown>): string[] {
  const messages: string[] = [];
  for (const nodeUpdate of Object.values(event)) {
    if (
      nodeUpdate &&
      typeof nodeUpdate === "object" &&
      "messages" in nodeUpdate &&
      Array.isArray((nodeUpdate as { messages: unknown }).messages)
    ) {
      for (const msg of (nodeUpdate as { messages: string[] }).messages) {
        if (typeof msg === "string") {
          messages.push(msg);
        }
      }
    }
  }
  return messages;
}

function extractDeckStructure(event: Record<string, unknown>): Slide[] | null {
  for (const nodeUpdate of Object.values(event)) {
    if (
      nodeUpdate &&
      typeof nodeUpdate === "object" &&
      "deck_structure" in nodeUpdate
    ) {
      const deck = (nodeUpdate as { deck_structure: Slide[] }).deck_structure;
      if (Array.isArray(deck) && deck.length > 0) {
        return deck;
      }
    }
  }
  return null;
}

export default function Home() {
  const [githubUrl, setGithubUrl] = useState("");
  const [status, setStatus] = useState<Status>("idle");
  const [progress, setProgress] = useState<string[]>([]);
  const [slides, setSlides] = useState<Slide[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [isDownloading, setIsDownloading] = useState(false);

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
      alert("Failed to download PowerPoint file.");
    } finally {
      setIsDownloading(false);
    }
  }

  async function handleGenerate() {
    const url = githubUrl.trim();
    if (!url) {
      setError("Please enter a GitHub repository URL.");
      setStatus("error");
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
    <div className="min-h-screen bg-slate-950 text-white">
      <main className="mx-auto max-w-5xl px-6 py-12">
        <header className="text-center mb-10">
          <h1 className="text-5xl font-bold">
            Welcome to <span className="text-blue-600">ShipDeck</span>
          </h1>
          <p className="mt-3 text-xl text-slate-300">
            Ship your idea faster. From code to deck in minutes.
          </p>
        </header>

        <section className="rounded-xl border border-slate-800 bg-slate-900/50 p-6">
          <label htmlFor="github-url" className="block text-sm font-medium text-slate-300 mb-2">
            GitHub repository URL
          </label>
          <div className="flex flex-col sm:flex-row gap-3">
            <input
              id="github-url"
              type="url"
              placeholder="https://github.com/owner/repo"
              value={githubUrl}
              onChange={(e) => setGithubUrl(e.target.value)}
              disabled={isGenerating}
              className="flex-1 rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-white placeholder:text-slate-500 focus:border-blue-600 focus:outline-none disabled:opacity-50"
            />
            <button
              onClick={handleGenerate}
              disabled={isGenerating}
              className="rounded-lg bg-blue-600 px-6 py-3 font-semibold hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap"
            >
              {isGenerating ? "Generating…" : "Generate deck"}
            </button>
          </div>
          {isGenerating && (
            <p className="mt-3 text-sm text-slate-400">
              Running agents… this may take 30–90 seconds.
            </p>
          )}
        </section>

        {error && (
          <div className="mt-6 rounded-lg border border-red-800 bg-red-950/50 px-4 py-3 text-red-300">
            {error}
          </div>
        )}

        {progress.length > 0 && (
          <section className="mt-8">
            <h2 className="text-lg font-semibold mb-3">Agent progress</h2>
            <ul className="rounded-xl border border-slate-800 bg-slate-900/50 p-4 space-y-2 max-h-64 overflow-y-auto">
              {progress.map((line, i) => (
                <li key={i} className="text-sm text-slate-300 font-mono">
                  {line}
                </li>
              ))}
            </ul>
          </section>
        )}

        {slides.length > 0 && (
          <section className="mt-8">
            <h2 className="text-lg font-semibold mb-3">
              Pitch deck ({slides.length} slides)
            </h2>
            <div className="grid gap-4 sm:grid-cols-2">
              {slides.map((slide) => (
                <article
                  key={slide.slide}
                  className="rounded-xl border border-slate-800 bg-slate-900/50 p-5 text-left"
                >
                  <span className="text-xs font-medium text-blue-500">
                    Slide {slide.slide}
                  </span>
                  <h3 className="mt-1 text-lg font-bold">{slide.title}</h3>
                  <p className="mt-2 text-sm text-slate-300 whitespace-pre-wrap">
                    {slide.content}
                  </p>
                </article>
              ))}
            </div>
          </section>
        )}

        {status === "done" && (
          <div className="mt-8 flex justify-center">
            {slides.length > 0 ? (
              <button
                onClick={handleDownload}
                disabled={isDownloading}
                className="rounded-lg bg-green-600 px-8 py-4 text-lg font-bold hover:bg-green-500 disabled:opacity-50 transition-colors shadow-lg"
              >
                {isDownloading ? "Preparing PPT..." : "Download Pitch Deck (PPTX)"}
              </button>
            ) : (
              <p className="text-slate-400">
                Generation finished but no slides were returned.
              </p>
            )}
          </div>
        )}
      </main>
    </div>
  );
}
