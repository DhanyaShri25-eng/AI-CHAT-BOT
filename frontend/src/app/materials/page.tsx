'use client';

import React, { useState, useEffect } from 'react';
import Navbar from '@/components/Navbar';
import { 
  Package, 
  Search, 
  Plus, 
  ShieldCheck, 
  MapPin, 
  Calendar
} from 'lucide-react';
import { MaterialCatalogItem } from '@/lib/types';
import { fetchMaterialsCatalog, submitPriceQuotationApi } from '@/lib/api';

export default function MaterialsPage() {
  const [materials, setMaterials] = useState<MaterialCatalogItem[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('All');
  const [searchQuery, setSearchQuery] = useState('');
  const [modalOpen, setModalOpen] = useState(false);
  const [newMaterial, setNewMaterial] = useState({
    name: '',
    category: 'Cement',
    unit_price: 400,
    supplier_name: '',
    location: 'Chennai'
  });

  const categories = ['All', 'Cement', 'Steel', 'Sand', 'Blocks', 'Tiles', 'Paint'];

  useEffect(() => {
    loadCatalog();
  }, [selectedCategory]);

  const loadCatalog = async () => {
    try {
      const cat = selectedCategory === 'All' ? undefined : selectedCategory;
      const res = await fetchMaterialsCatalog(cat);
      setMaterials(res);
    } catch (err) {
      console.error(err);
    }
  };

  const handleAddQuotation = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await submitPriceQuotationApi({
        material_name: newMaterial.name,
        unit_price: Number(newMaterial.unit_price),
        supplier_name: newMaterial.supplier_name,
        location: newMaterial.location
      });
      setModalOpen(false);
      loadCatalog();
    } catch (err) {
      console.error(err);
    }
  };

  const filtered = materials.filter((m) =>
    m.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    m.category.toLowerCase().includes(searchQuery.toLowerCase()) ||
    m.supplier.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col">
      <Navbar />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 w-full flex-1 space-y-6">
        
        {/* Page Header */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-4 border-b border-slate-200">
          <div>
            <h1 className="text-2xl font-black text-slate-900 flex items-center gap-2.5">
              <span className="p-2 rounded-xl bg-blue-50 border border-blue-200 text-blue-600 shadow-2xs">
                <Package className="w-5 h-5" />
              </span>
              Material Catalog &amp; Supplier Quotations
            </h1>
            <p className="text-xs text-slate-600 mt-1">
              Verified market prices for ISI-grade structural civil materials in South India (Q3 2026).
            </p>
          </div>

          <button
            onClick={() => setModalOpen(true)}
            className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold shadow-xs transition"
          >
            <Plus className="w-4 h-4" />
            Add Supplier Quotation
          </button>
        </div>

        {/* Filters and Search Bar */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-3">
          {/* Category Pills */}
          <div className="flex items-center gap-1.5 overflow-x-auto w-full sm:w-auto">
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition whitespace-nowrap border ${
                  selectedCategory === cat
                    ? 'bg-blue-50 border-blue-300 text-blue-700 font-bold shadow-2xs'
                    : 'bg-white border-slate-200 text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>

          {/* Search Box */}
          <div className="relative w-full sm:w-64">
            <Search className="w-3.5 h-3.5 absolute left-3 top-2.5 text-slate-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search material or supplier..."
              className="w-full bg-white border border-slate-300 rounded-xl pl-8 pr-3 py-1.5 text-xs text-slate-900 placeholder-slate-400 focus:outline-none focus:border-blue-600 transition shadow-2xs"
            />
          </div>
        </div>

        {/* Material Items Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtered.map((item) => (
            <div
              key={item.id}
              className="bg-white border border-slate-200 hover:border-blue-300 shadow-sm hover:shadow-md p-5 rounded-2xl flex flex-col justify-between space-y-4 transition"
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded bg-blue-50 border border-blue-200 text-blue-700">
                    {item.category}
                  </span>
                  <span className="text-[11px] text-emerald-700 font-semibold flex items-center gap-1">
                    <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" /> Verified
                  </span>
                </div>

                <h3 className="text-sm font-bold text-slate-900 mb-1">
                  {item.name}
                </h3>
                <p className="text-xs text-slate-500">
                  {item.specification || 'IS Standard Conforming'}
                </p>
              </div>

              <div className="pt-3 border-t border-slate-100 space-y-2 text-xs">
                <div className="flex items-center justify-between">
                  <span className="text-slate-500">Unit Price:</span>
                  <span className="text-base font-extrabold text-blue-700 font-mono">
                    ₹{item.default_price.toLocaleString()}{' '}
                    <span className="text-[11px] text-slate-500 font-normal">/ {item.unit}</span>
                  </span>
                </div>

                <div className="flex items-center justify-between text-[11px] text-slate-500">
                  <span className="flex items-center gap-1">
                    <MapPin className="w-3 h-3 text-slate-400" /> {item.location}
                  </span>
                  <span className="flex items-center gap-1">
                    <Calendar className="w-3 h-3 text-slate-400" /> {item.quotation_date}
                  </span>
                </div>

                <div className="text-[11px] text-slate-700 font-medium truncate pt-1">
                  Supplier: {item.supplier}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Add Quotation Modal */}
      {modalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm">
          <div className="w-full max-w-md bg-white border border-slate-200 rounded-2xl shadow-2xl p-6 relative">
            <h3 className="text-base font-bold text-slate-900 mb-4">
              Submit Verified Supplier Quotation
            </h3>

            <form onSubmit={handleAddQuotation} className="space-y-3.5 text-xs">
              <div>
                <label className="text-slate-700 font-medium block mb-1">Material Name &amp; Grade</label>
                <input
                  type="text"
                  required
                  value={newMaterial.name}
                  onChange={(e) => setNewMaterial({ ...newMaterial, name: e.target.value })}
                  placeholder="e.g. UltraTech Super 53 Grade"
                  className="w-full bg-slate-50 border border-slate-300 rounded-lg p-2 text-slate-900 focus:bg-white focus:border-blue-600 focus:outline-none"
                />
              </div>

              <div>
                <label className="text-slate-700 font-medium block mb-1">Category</label>
                <select
                  value={newMaterial.category}
                  onChange={(e) => setNewMaterial({ ...newMaterial, category: e.target.value })}
                  className="w-full bg-slate-50 border border-slate-300 rounded-lg p-2 text-slate-900 focus:bg-white focus:border-blue-600 focus:outline-none"
                >
                  {categories.filter((c) => c !== 'All').map((c) => (
                    <option key={c} value={c}>{c}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="text-slate-700 font-medium block mb-1">Unit Price (INR)</label>
                <input
                  type="number"
                  required
                  value={newMaterial.unit_price}
                  onChange={(e) => setNewMaterial({ ...newMaterial, unit_price: Number(e.target.value) })}
                  className="w-full bg-slate-50 border border-slate-300 rounded-lg p-2 text-slate-900 focus:bg-white focus:border-blue-600 focus:outline-none"
                />
              </div>

              <div>
                <label className="text-slate-700 font-medium block mb-1">Supplier Name</label>
                <input
                  type="text"
                  required
                  value={newMaterial.supplier_name}
                  onChange={(e) => setNewMaterial({ ...newMaterial, supplier_name: e.target.value })}
                  placeholder="e.g. Annai Builders Depot"
                  className="w-full bg-slate-50 border border-slate-300 rounded-lg p-2 text-slate-900 focus:bg-white focus:border-blue-600 focus:outline-none"
                />
              </div>

              <div className="flex justify-end gap-2 pt-3 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setModalOpen(false)}
                  className="px-3.5 py-1.5 rounded-lg text-slate-600 hover:text-slate-900 hover:bg-slate-100 font-medium"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-700 text-white font-semibold shadow-xs"
                >
                  Save Quotation
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
