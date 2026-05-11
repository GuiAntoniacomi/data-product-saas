'use client'

import { useState } from 'react'
import { TrendingUp, DollarSign, Star, AlertCircle, PackageSearch } from 'lucide-react'
import { clsx } from 'clsx'

type Product = {
  id: string
  name: string
  aliexpress_price: number
  estimated_amazon_price: number
  margin_pct: number
  reviews_count: number
  rating: number
  monthly_orders: number
  score: number
  category: string
  aliexpress_url: string
  search_keyword: string
}

const CATEGORIES = ['Todos', 'Casa e Cozinha', 'Pets', 'Fitness', 'Jardim', 'Ferramentas']

function ScoreBadge({ score }: { score: number }) {
  return (
    <span className={clsx(
      'inline-flex items-center rounded px-2 py-0.5 text-xs font-bold',
      score >= 85 ? 'bg-emerald-500/20 text-emerald-400' :
      score >= 70 ? 'bg-yellow-500/20 text-yellow-400' :
      'bg-red-500/20 text-red-400'
    )}>
      {score}
    </span>
  )
}

function MarginBadge({ pct }: { pct: number }) {
  return (
    <span className={clsx(
      'inline-flex items-center gap-1 rounded px-2 py-0.5 text-xs font-medium',
      pct >= 45 ? 'bg-emerald-500/10 text-emerald-400' :
      pct >= 30 ? 'bg-blue-500/10 text-blue-400' :
      'bg-zinc-500/10 text-zinc-400'
    )}>
      <DollarSign size={10} />{pct}%
    </span>
  )
}

export function ProductTable({ products }: { products: Product[] }) {
  const [query, setQuery] = useState('')
  const [category, setCategory] = useState('Todos')
  const [minMargin, setMinMargin] = useState(25)

  const filtered = products.filter(p => {
    const matchQuery = p.name.toLowerCase().includes(query.toLowerCase())
    const matchCategory = category === 'Todos' || p.category === category
    const matchMargin = p.margin_pct >= minMargin
    return matchQuery && matchCategory && matchMargin
  })

  if (products.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-24 text-center">
        <PackageSearch size={40} className="text-zinc-600 mb-4" />
        <p className="text-zinc-400 font-medium">Nenhum produto ainda</p>
        <p className="text-zinc-600 text-sm mt-1">
          Clique em <span className="text-violet-400">Executar Scraper</span> para buscar produtos no AliExpress
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {/* Filtros */}
      <div className="flex flex-wrap gap-3 items-end">
        <div className="relative flex-1 min-w-[200px]">
          <input
            type="text"
            value={query}
            onChange={e => setQuery(e.target.value)}
            placeholder="Buscar produto..."
            className="w-full rounded-md border border-zinc-700 bg-zinc-900 px-3 py-2 text-sm text-white placeholder-zinc-500 focus:border-violet-500 focus:outline-none"
          />
        </div>
        <select
          value={category}
          onChange={e => setCategory(e.target.value)}
          className="rounded-md border border-zinc-700 bg-zinc-900 px-3 py-2 text-sm text-white focus:border-violet-500 focus:outline-none"
        >
          {CATEGORIES.map(c => <option key={c}>{c}</option>)}
        </select>
        <div className="flex items-center gap-2">
          <label className="text-xs text-zinc-400 whitespace-nowrap">Margem mín.</label>
          <input
            type="number"
            value={minMargin}
            onChange={e => setMinMargin(Number(e.target.value))}
            min={0} max={100}
            className="w-16 rounded-md border border-zinc-700 bg-zinc-900 px-2 py-2 text-sm text-white focus:border-violet-500 focus:outline-none"
          />
          <span className="text-xs text-zinc-500">%</span>
        </div>
      </div>

      {/* Aviso dados reais */}
      {products.some(p => p.search_keyword === 'demo') && (
        <div className="flex items-center gap-2 rounded-md border border-yellow-700/50 bg-yellow-900/20 px-4 py-2.5 text-sm text-yellow-400">
          <AlertCircle size={14} />
          <span>Dados de demonstração — execute o scraper para substituir por produtos reais do AliExpress.</span>
        </div>
      )}
      {!products.some(p => p.search_keyword === 'demo') && (
        <div className="flex items-center gap-2 rounded-md border border-zinc-700/50 bg-zinc-900/50 px-4 py-2.5 text-sm text-zinc-400">
          <AlertCircle size={14} />
          <span>Preços Amazon são estimativas baseadas em múltiplos por categoria. Execute o scraper para atualizar.</span>
        </div>
      )}

      {/* Tabela */}
      <div className="rounded-lg border border-zinc-800 overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-zinc-900 border-b border-zinc-800">
            <tr>
              <th className="text-left px-4 py-3 text-xs font-medium text-zinc-400 uppercase tracking-wide">Produto</th>
              <th className="text-right px-4 py-3 text-xs font-medium text-zinc-400 uppercase tracking-wide">AliExpress</th>
              <th className="text-right px-4 py-3 text-xs font-medium text-zinc-400 uppercase tracking-wide">Amazon est.</th>
              <th className="text-center px-4 py-3 text-xs font-medium text-zinc-400 uppercase tracking-wide">Margem</th>
              <th className="text-right px-4 py-3 text-xs font-medium text-zinc-400 uppercase tracking-wide">Pedidos/mês</th>
              <th className="text-center px-4 py-3 text-xs font-medium text-zinc-400 uppercase tracking-wide w-16">Score</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-800">
            {filtered.length === 0 ? (
              <tr>
                <td colSpan={6} className="text-center py-12 text-zinc-500">
                  Nenhum produto com esses filtros.
                </td>
              </tr>
            ) : (
              filtered.map(product => (
                <tr key={product.id} className="bg-zinc-900/50 hover:bg-zinc-800/60 transition-colors">
                  <td className="px-4 py-3">
                    <div>
                      <a
                        href={product.aliexpress_url || '#'}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="font-medium text-zinc-100 hover:text-violet-300 transition-colors"
                      >
                        {product.name}
                      </a>
                      <div className="flex items-center gap-2 mt-1">
                        <span className="text-xs text-zinc-500">{product.category}</span>
                        <span className="text-xs text-zinc-600">·</span>
                        <span className="flex items-center gap-0.5 text-xs text-zinc-500">
                          <Star size={10} className="text-yellow-500 fill-yellow-500" />
                          {product.rating} ({product.reviews_count?.toLocaleString()} reviews)
                        </span>
                      </div>
                    </div>
                  </td>
                  <td className="px-4 py-3 text-right text-zinc-300 font-mono">
                    ${product.aliexpress_price?.toFixed(2)}
                  </td>
                  <td className="px-4 py-3 text-right text-zinc-300 font-mono">
                    ${product.estimated_amazon_price?.toFixed(2)}
                  </td>
                  <td className="px-4 py-3 text-center">
                    <MarginBadge pct={product.margin_pct} />
                  </td>
                  <td className="px-4 py-3 text-right">
                    <span className="flex items-center justify-end gap-1 text-zinc-300">
                      <TrendingUp size={12} className="text-emerald-500" />
                      {product.monthly_orders?.toLocaleString()}
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
