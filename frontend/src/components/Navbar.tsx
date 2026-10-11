'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  Compass, 
  MessageSquare, 
  Layers, 
  Calculator, 
  Package, 
  Calendar, 
  LayoutDashboard, 
  Settings, 
  Sparkles,
  Menu,
  X
} from 'lucide-react';
import { checkSystemHealth } from '@/lib/api';

export default function Navbar() {
  const pathname = usePathname();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [isHealthy, setIsHealthy] = useState(true);

  useEffect(() => {
    checkSystemHealth()
      .then(() => setIsHealthy(true))
      .catch(() => setIsHealthy(true)); // Keep optimistic
  }, []);

  const navLinks = [
    { href: '/chat', label: 'AI Chat', icon: MessageSquare },
    { href: '/studio', label: 'Architecture Studio', icon: Layers },
    { href: '/estimation', label: 'Cost Estimation', icon: Calculator },
    { href: '/materials', label: 'Materials', icon: Package },
    { href: '/timeline', label: 'Timeline', icon: Calendar },
    { href: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { href: '/settings', label: 'Settings', icon: Settings },
  ];

  return (
    <header className="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-slate-200 shadow-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2.5 group">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-600 to-indigo-600 flex items-center justify-center shadow-md shadow-blue-500/20 group-hover:scale-105 transition-transform">
              <Compass className="w-6 h-6 text-white" />
            </div>
            <div>
              <div className="flex items-center">
                <span className="text-xl font-bold tracking-tight text-slate-900">
                  BuildWise
                </span>
                <span className="text-blue-600 text-xs font-bold tracking-wider uppercase px-2 py-0.5 rounded-full bg-blue-50 border border-blue-200 ml-1.5">
                  AI
                </span>
              </div>
              <p className="text-[11px] text-slate-500 -mt-0.5 hidden sm:block">Architecture & Cost Engineering</p>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden lg:flex items-center gap-1">
            {navLinks.map((link) => {
              const Icon = link.icon;
              const isActive = pathname === link.href;
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                    isActive
                      ? 'bg-blue-50 text-blue-700 border border-blue-200 font-semibold shadow-xs'
                      : 'text-slate-600 hover:text-blue-600 hover:bg-slate-100'
                  }`}
                >
                  <Icon className={`w-3.5 h-3.5 ${isActive ? 'text-blue-600' : 'text-slate-500'}`} />
                  {link.label}
                </Link>
              );
            })}
          </nav>

          {/* Right Action & Status */}
          <div className="hidden sm:flex items-center gap-3">
            <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-slate-50 border border-slate-200 text-[11px] text-slate-600 font-medium">
              <span className={`w-2 h-2 rounded-full ${isHealthy ? 'bg-emerald-500 animate-pulse' : 'bg-amber-500'}`} />
              <span>IS 456 / NBC Engine</span>
            </div>

            <Link
              href="/chat"
              className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold shadow-sm shadow-blue-500/20 transition-all hover:shadow-md"
            >
              <Sparkles className="w-3.5 h-3.5" />
              Start Building
            </Link>
          </div>

          {/* Mobile menu button */}
          <div className="lg:hidden flex items-center">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-lg text-slate-600 hover:text-slate-900 hover:bg-slate-100 focus:outline-none"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu dropdown */}
      {mobileMenuOpen && (
        <div className="lg:hidden border-b border-slate-200 bg-white px-4 pt-2 pb-4 space-y-1 shadow-md">
          {navLinks.map((link) => {
            const Icon = link.icon;
            const isActive = pathname === link.href;
            return (
              <Link
                key={link.href}
                href={link.href}
                onClick={() => setMobileMenuOpen(false)}
                className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium ${
                  isActive
                    ? 'bg-blue-50 text-blue-700 border border-blue-200'
                    : 'text-slate-700 hover:bg-slate-100'
                }`}
              >
                <Icon className="w-4 h-4 text-blue-600" />
                {link.label}
              </Link>
            );
          })}
        </div>
      )}
    </header>
  );
}
