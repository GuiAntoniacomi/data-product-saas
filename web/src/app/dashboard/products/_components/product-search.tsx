'use client'

import { useState } from 'react'
import { Search, TrendingUp, DollarSign, Star, AlertCircle } from 'lucide-react'
import { clsx } from 'clsx'

type Product = {
  id: string
  name: string
  aliexpressPrice: number
  estimatedAmazonPrice: number
  marginPct: number
  reviews: number
  rating: number
  monthlySales: number
  score: number
  category: string
  link: string
  alert?: string
}

const CATEGORIES = [
  'Todos',
  'Casa e Cozinha',
  'Eletrônicos',
  'Jardim',
  'Pets',
  'Fitness',
  'Beleza',
  'Ferramentas',
]

const MOCK_PRODUCTS: Product[] = [
  {
    id: '1',
    name: 'Organizador de gaveta em bambu (15cm × 30cm)',
    aliexpressPrice: 4.2,
    estimatedAmazonPrice: 18.99,
    marginPct: 42,
    reviews: 1840,
    rating: 4.6,
    monthlySales: 3200,
    score: 87,
    category: 'Casa e Cozinha',
    link: '#',
  },
  {
    id: '2',
    name: 'Suporte de telefone para carro com ventosa magnética',
    aliexpressPrice: 2.8,
    estimatedAmazonPrice: 14.99,
    marginPct: 38,
    reviews: 9200,
    rating: 4.4,
    monthlySales: 5800,
    score: 74,
    category: 'Eletrônicos',
    link: '#',
    alert: 'Alta concorrência (42 vendedores)',
  },
  {
    id: '3',
    name: 'Bebedouro automático para pets com filtro',
    aliexpressPrice: 11.5,
    estimatedAmazonPrice: 39.99,
    marginPct: 51,
    reviews: 430,
    rating: 4.8,
    monthlySales: 980,
    score: 91,
    category: 'Pets',
    link: '#',
  },
  {
    id: '4',
    name: 'Faixa de resistência para treino (kit 5 níveis)',
    aliexpressPrice: 6.1,
    estimatedAmazonPrice: 22.99,
    marginPct: 44,
    reviews: 2100,
    rating: 4.5,
    monthlySales: 4400,
    score: 82,
    category: 'Fitness',
    link: '#',
  },
  {
    id: '5',
    name: 'Esfoliante elétrico de pés USB',
    aliexpressPrice: 7.9,
    estimatedAmazonPrice: 29.99,
    marginPct: 47,
    reviews: 670,
    rating: 4.3,
    monthlySales: 1500,
    score: 79,
    category: 'Beleza',
    link: '#',
  },
]

function ScoreBadge({ score }: { score: number }) {
  return (
    <span
      className={clsx(
        'inline-flex items-center rounded px-2 py-0.5 text-xs font-bold',
        score >= 85 ? 'bg-emerald-500/20 text-emerald-400' :
        score >= 70 ? 'bg-yellow-500/20 text-yellow-400' :
        'bg-red-500/20 text-red-400'
      )}
    >
      {score}
    </span>
  )
}

function MarginBadge({ pct }: { pct: number }) {
  return (
    <span
      className={clsx(
        'inline-flex items-center gap-1 rounded px-2 py-0.5 text-xs font-medium',
        pct >= 45 ? 'bg-emerald-500/10 text-emerald-400' :
        pct >= 30 ? 'bg-blue-500/10 text-blue-400' :
        'bg-zinc-500/10 text-zinc-400'
      )}
    >
      <DollarSign size={10} />
      {pct}%
    </span>
  )
}

export function ProductSearch() {
  const [query, setQuery] = useState('')
  const [category, setCategory] = useState('Todos')
  const [minMargin, setMinMargin] = useState(30)
  const [minScore, setMinScore] = useState(0)

  const filtered = MOCK_PRODUCTS.filter((p) => {
    const matchQuery = p.name.toLowerCase().includes(query.toLowerCase())
    const matchCategory = category === 'Todos' || p.category === category
    const matchMargin = p.marginPct >= minMargin
    const matchScore = p.score >= minScore
    return matchQuery && matchCategory && matchMargin && matchScore
  }).sort((a, b) => b.score - a.score)

  return (
    <div className="space-y-5">
      {/* Filtros */}
      <div className="flex flex-wrap gap-3 items-end">
        <div className="relative flex-1 min-w-[200px]">
          <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-500" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Buscar produto..."
            className="w-full rounded-md border border-zinc-700 bg-zinc-900 pl-8 pr-3 py-2 text-sm text-white placeholder-zinc-500 focus:border-violet-500 focus:outline-none"
          />
        </div>

        <select
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          className="rounded-md border border-zinc-700 bg-zinc-900 px-3 py-2 text-sm text-white focus:border-violet-500 focus:outline-none"
        >
          {CATEGORIES.map((c) => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>

        <div className="flex items-center gap-2">
          <label className="text-xs text-zinc-400 whitespace-nowrap">Margem mín.</label>
          <input
            type="number"
            value={minMargin}
            onChange={(e) => setMinMargin(Number(e.target.value))}
            min={0}
            max={100}
            className="w-16 rounded-md border border-zinc-700 bg-zinc-900 px-2 py-2 text-sm text-white focus:border-violet-500 focus:outline-none"
          />
          <span className="text-xs text-zinc-500">%</span>
        </div>

        <div className="flex items-center gap-2">
          <label className="text-xs text-zinc-400 whitespace-nowrap">Score mín.</label>
          <input
            type="number"
            value={minScore}
            onChange={(e) => setMinScore(Number(e.target.value))}
            min={0}
            max={100}
            className="w-16 rounded-md border border-zinc-700 bg-zinc-900 px-2 py-2 text-sm text-white focus:border-violet-500 focus:outline-none"
          />
        </div>
      </div>

      {/* Aviso dados mock */}
      <div className="flex items-center gap-2 rounded-md border border-yellow-800/50 bg-yellow-900/10 px-4 py-2.5 text-sm text-yellow-400">
        <AlertCircle size={14} />
        <span>Dados de demonstração — conecte a AliExpress API e Keepa API para dados reais.</span>
      </div>

      {/* Tabela */}
      <div className="rounded-lg border border-zinc-800 overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-zinc-900 border-b border-zinc-800">
            <tr>
              <th className="text-left px-4 py-3 text-xs font-medium text-zinc-400 uppercase tracking-wide">Produto</th>
              <th className="text-right px-4 py-3 text-xs font-medium text-zinc-400 uppercase tracking-wide">AliExpress</th>
              <th className="text-right px-4 py-3 text-xs font-medium text-zinc-400 uppercase tracking-wide">Amazon est.</th>
              <th className="text-center px-4 py-3 text-xs font-medium text-zinc-400 uppercase tracking-wide">Margem</th>
              <th className="text-right px-4 py-3 text-xs font-medium text-zinc-400 uppercase tracking-wide">Vendas/mês</th>
              <th className="text-center px-4 py-3 text-xs font-medium text-zinc-400 uppercase tracking-wide w-16">Score</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-800">
            {filtered.length === 0 ? (
              <tr>
                <td colSpan={6} className="text-center py-12 text-zinc-500">
                  Nenhum produto encontrado com esses filtros.
                </td>
              </tr>
            ) : (
              filtered.map((product) => (
                <tr key={product.id} className="bg-zinc-900/50 hover:bg-zinc-800/60 transition-colors">
                  <td className="px-4 py-3">
                    <div>
                      <p className="font-medium text-zinc-100">{product.name}</p>
                      <div className="flex items-center gap-2 mt-1">
                        <span className="text-xs text-zinc-500">{product.category}</span>
                        <span className="text-xs text-zinc-600">·</span>
                        <span className="flex items-center gap-0.5 text-xs text-zinc-500">
                          <Star size={10} className="text-yellow-500 fill-yellow-500" />
                          {product.rating} ({product.reviews.toLocaleString()} reviews)
                        </span>
                        {product.alert && (
                          <>
                            <span className="text-xs text-zinc-600">·</span>
                            <span className="text-xs text-amber-500">{product.alert}</span>
                          </>
                        )}
                      </div>
                    </div>
                  </td>
                  <td className="px-4 py-3 text-right text-zinc-300 font-mono">
                    ${product.aliexpressPrice.toFixed(2)}
                  </td>
                  <td className="px-4 py-3 text-right text-zinc-300 font-mono">
                    ${product.estimatedAmazonPrice.toFixed(2)}
                  </td>
                  <td className="px-4 py-3 text-center">
                    <MarginBadge pct={product.marginPct} />
                  </td>
                  <td className="px-4 py-3 text-right">
                    <span className="flex items-center justify-end gap-1 text-zinc-300">
                      <TrendingUp size={12} className="text-emerald-500" />
                      {product.monthlySales.toLocaleString()}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-center">
                    <ScoreBadge score={product.score} />
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      <p className="text-xs text-zinc-600">
        {filtered.length} produto{filtered.length !== 1 ? 's' : ''} · ordenados por score
      </p>
    </div>
  )
}
