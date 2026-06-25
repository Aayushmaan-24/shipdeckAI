"use client";

import { motion } from "framer-motion";
import { Code2, Layout, Zap, Cpu, ShieldCheck, Globe } from "lucide-react";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

const features = [
  {
    icon: <Code2 className="h-6 w-6 text-blue-500" />,
    title: "Repo Intelligence",
    description: "Deep codebase analysis to extract architecture, tech stack, and core logic."
  },
  {
    icon: <Cpu className="h-6 w-6 text-indigo-500" />,
    title: "Multi-Agent System",
    description: "Specialized AI agents working together as architects, strategists, and designers."
  },
  {
    icon: <Layout className="h-6 w-6 text-cyan-500" />,
    title: "Modern Layouts",
    description: "Professionally designed PPTX templates with consistent typography and spacing."
  },
  {
    icon: <Zap className="h-6 w-6 text-yellow-500" />,
    title: "Instant Export",
    description: "Go from GitHub URL to a production-ready PowerPoint file in under 90 seconds."
  },
  {
    icon: <ShieldCheck className="h-6 w-6 text-emerald-500" />,
    title: "Zero Hallucination",
    description: "Strict cross-verification ensures every slide is grounded in your actual code."
  },
  {
    icon: <Globe className="h-6 w-6 text-rose-500" />,
    title: "Pitch Ready",
    description: "Structured for VCs and stakeholders with mandatory sections like Problem and Roadmap."
  }
];

export function Features() {
  return (
    <section className="py-20 bg-slate-950/50">
      <div className="container mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">Powerful Features for Founders</h2>
          <p className="text-slate-400 max-w-xl mx-auto">Everything you need to transform technical complexity into a compelling narrative.</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: i * 0.1 }}
            >
              <Card className="h-full bg-slate-900/50 border-slate-800 hover:border-slate-700 transition-colors shadow-none">
                <CardHeader>
                  <div className="mb-4">{feature.icon}</div>
                  <CardTitle className="text-xl text-white mb-2">{feature.title}</CardTitle>
                  <CardDescription className="text-slate-400 leading-relaxed">{feature.description}</CardDescription>
                </CardHeader>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
