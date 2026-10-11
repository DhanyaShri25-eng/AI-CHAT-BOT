import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "BuildWise AI - AI-Powered Architectural Design, Estimation & Planning",
  description: "Conversational AI platform for building construction, Vastu-compliant 2D floor plans, deterministic IS 456 material estimation, itemized project costing, and CPM scheduling with Tamil and Tanglish voice support.",
  keywords: ["construction AI", "floor plan generator", "IS 456 civil estimate", "Tamil construction chatbot", "Gantt schedule AI", "BuildWise AI"]
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col bg-slate-50 text-slate-900">
        {children}
      </body>
    </html>
  );
}
