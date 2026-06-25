"use client";

import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { ArrowRight, Github } from "lucide-react";

export function Hero() {
  return (
    <section className="relative overflow-hidden pt-24 pb-16 md:pt-32 md:pb-24">
      {/* Background Glow */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-7xl h-full -z-10">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-blue-600/20 blur-[120px] rounded-full" />
        <div className="absolute bottom-[10%] right-[-5%] w-[30%] h-[30%] bg-indigo-600/10 blur-[100px] rounded-full" />
      </div>

      <div className="container mx-auto px-6 text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight text-white mb-6">
            From Code to <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-indigo-500">Investor Deck</span> in Minutes
          </h1>
          <p className="text-xl text-slate-400 max-w-2xl mx-auto mb-10">
            ShipDeck uses multi-agent AI to analyze your GitHub repository and craft a professional, data-driven pitch deck that captures your project&apos;s essence.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Button asChild size="lg" className="rounded-full px-8 h-12 text-base font-semibold group">
              <a href="#generator">
                Start Building <ArrowRight className="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
              </a>
            </Button>
            <Button asChild size="lg" variant="outline" className="rounded-full px-8 h-12 text-base font-semibold border-slate-800 bg-slate-950/50 hover:bg-slate-900 transition-colors">
              <a href="https://github.com/Aayushmaan-24/shipdeckAI" target="_blank" rel="noopener noreferrer">
                <Github className="mr-2 h-5 w-5" /> View on GitHub
              </a>
            </Button>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
