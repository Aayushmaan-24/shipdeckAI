import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ShipDeck - From Code to Pitch Deck in Minutes",
  description: "Instantly transform any GitHub repository or ZIP codebase into a highly visual, investor-grade pitch deck.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
