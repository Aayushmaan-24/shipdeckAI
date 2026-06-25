"use client";

import { Search, BrainCircuit, Presentation, Download } from "lucide-react";

const steps = [
  {
    icon: <Search className="h-5 w-5" />,
    title: "1. Paste URL",
    description: "Provide your public GitHub repository link."
  },
  {
    icon: <BrainCircuit className="h-5 w-5" />,
    title: "2. AI Analysis",
    description: "Our agents explore files, READMEs, and metadata."
  },
  {
    icon: <Presentation className="h-5 w-5" />,
    title: "3. Slide Generation",
    description: "Multi-agent orchestration builds your deck structure."
  },
  {
    icon: <Download className="h-5 w-5" />,
    title: "4. Download PPTX",
    description: "Get your polished PowerPoint file ready to ship."
  }
];

export function Workflow() {
  return (
    <section className="py-20 border-t border-slate-900 bg-slate-950">
      <div className="container mx-auto px-6">
        <div className="flex flex-col md:flex-row items-center justify-between gap-12">
          <div className="max-w-md">
            <h2 className="text-3xl font-bold text-white mb-6 text-center md:text-left">Simple, Automated Workflow</h2>
            <p className="text-slate-400 mb-8 leading-relaxed text-center md:text-left">
              ShipDeck automates the tedious parts of startup preparation. Focus on your code while we handle the business narrative and visual presentation.
            </p>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 w-full max-w-2xl">
            {steps.map((step, i) => (
              <div key={i} className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800/50">
                <div className="w-10 h-10 rounded-full bg-blue-600/10 flex items-center justify-center text-blue-500 mb-4">
                  {step.icon}
                </div>
                <h3 className="text-lg font-semibold text-white mb-2">{step.title}</h3>
                <p className="text-sm text-slate-400">{step.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
