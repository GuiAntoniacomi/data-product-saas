'use client'

import { useState } from 'react'
import { ExternalLink, ChevronLeft, ChevronRight } from 'lucide-react'
import { clsx } from 'clsx'

type TrendSignal = {
  id: string
  source: string
  product_name: string
  category: string | null
  signal_text: string | null
  opportunity_score: number | null
  trend_strength: number | null
  lead_time_days: number | null
  subreddit: string | null
  source_url: string | null
  scraped_at: string
}

const PAGE_SIZE = 25

function ScoreBadge({ score }: { score: number | null }) {
  if (score === null) return null
  const color =
    score >= 70 ? 'bg-emerald-500/15 text-emerald-400' :
    score >= 50 ? 'bg-yellow-500/15 text-yellow-400' :
                  'bg-zinc-700 text-zinc-400'
  return (
    <span className={clsx('inline-flex items-center rounded px-2 py-0.5 text-xs font-semibold tabular-nums', color)}>
      {score}
    </span>
  )
}

function SourceBadge({ source }: { source: string }) {
  const isReddit = source === 'reddit'
  return (
    <span className={clsx(
      'inline-flex items-center rounded px-2 py-0.5 text-xs font-medium',
      isReddit ? 'bg-orange-500/15 text-orange-400' : 'bg-blue-500/15 text-blue-400'
    )}>
      {isReddit ? 'Reddit' : 'Google Trends'}
    </span>
  )
}

function LeadTimeBadge({ days }: { days: number | null }) {
  if (!days) return null
  return (
    <span className="inline-flex items-center rounded bg-violet-500/15 px-2 py-0.5 text-xs text-violet-400">
      {days}d lead
    </span>
  )
}

export function TrendTable({ signals }: { signals: TrendSignal[] }) {
  const [query, setQuery] = useState('')
  const [source, setSource] = useState('all')
  const [category, setCategory] = useState('all')
  const [page, setPage] = useState(1)

  const categories = Array.from(new Set(signals.map(s => s.category).filter(Boolean))) as string[]

  const filtered = signals.filter(s => {
    const matchQuery = !query || s.product_name.toLowerCase().includes(query.toLowerCase())
    const matchSource = source === 'all' || s.source === source
    const matchCategory = category === 'all' || s.category === category
    return matchQuery && matchSource && matchCategory
  })

  const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE))
  const paginated = filtered.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE)

  function handleFilter(fn: () => void) {
    fn()
    setPage(1)
  }

  if (signals.length === 0) {
    return (
      <div className="rounded-lg border border-dashed border-zinc-700 p-12 text-center">
        <p className="text-zinc-500 text-sm">Nenhum sinal ainda — execute a análise para começar.</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {/* Filters */}
      <div className="flex flex-wrap items-center gap-3">
        <input
          type="text"
          placeholder="Buscar produto..."
          value={query}
          onChange={e => handleFilter(() => setQuery(e.target.value))}
          className="rounded-md border border-zinc-700 bg-zinc-800 px-3 py-1.5 text-sm text-white placeholder:text-zinc-500 focus:border-violet-500 focus:outline-none w-48"
        />
        <select
          value={source}
          onChange={e => handleFilter(() => setSource(e.target.value))}
          className="rounded-md border border-zinc-700 bg-zinc-800 px-3 py-1.5 text-sm text-white focus:border-violet-500 focus:outline-none"
        >
          <option value="all">Todas as fontes</option>
          <option value="reddit">Reddit</option>
          <option value="google_trends">Google Trends</option>
        </select>
        <select
          value={category}
          onChange={e => handleFilter(() => setCategory(e.target.value))}
          className="rounded-md border border-zinc-700 bg-zinc-800 px-3 py-1.5 text-sm text-white focus:border-violet-500 focus:outline-none"
        >
          <option value="all">Todas as categorias</option>
          {categories.map(c => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>
        <span className="ml-auto text-xs text-zinc-500">{filtered.length} oportunidades</span>
      </div>

      {/* Table */}
      <div className="overflow-x-auto rounded-lg border border-zinc-800">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-zinc-800 bg-zinc-900">
              <th className="px-4 py-3 text-left text-xs font-medium text-zinc-400">Produto</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-zinc-400">Categoria</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-zinc-400">Fonte</th>
              <th className="px-4 py-3 text-right text-xs font-medium text-zinc-400">Score</th>
              <th className="px-4 py-3 text-right text-xs font-medium text-zinc-400">Força</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-zinc-400">Lead Time</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-zinc-400 max-w-xs">Sinal</th>
              <th className="px-4 py-3 text-center text-xs font-medium text-zinc-400">Link</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-800">
            {paginated.map(signal => (
              <tr key={signal.id} className="bg-zinc-950 hover:bg-zinc-900/60 transition-colors">
                <td className="px-4 py-3 font-medium text-white max-w-[220px]">
                  <span className="line-clamp-2">{signal.product_name}</span>
                </td>
                <td className="px-4 py-3 text-zinc-400 whitespace-nowrap">
                  {signal.category ?? '—'}
                </td>
                <td className="px-4 py-3">
                  <SourceBadge source={signal.source} />
                </td>
                <td className="px-4 py-3 text-right">
                  <ScoreBadge score={signal.opportunity_score} />
                </td>
                <td className="px-4 py-3 text-right tabular-nums text-zinc-400">
                  {signal.trend_strength ?? '—'}
                </td>
                <td className="px-4 py-3">
                  <LeadTimeBadge days={signal.lead_time_days} />
                </td>
                <td className="px-4 py-3 text-zinc-500 text-xs max-w-[280px]">
                  <span className="line-clamp-2">{signal.signal_text ?? '—'}</span>
                </td>
                <td className="px-4 py-3 text-center">
                  {signal.source_url ? (
                    <a
                      href={signal.source_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex text-zinc-500 hover:text-violet-400 transition-colors"
                    >
                      <ExternalLink size={14} />
                    </a>
                  ) : (
                    <span className="text-zinc-700">—</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex items-center justify-between text-xs text-zinc-500">
          <span>Página {page} de {totalPages}</span>
          <div className="flex gap-1">
            <button
              onClick={() => setPage(p => Math.max(1, p - 1))}
              disabled={page === 1}
              className="rounded p-1 hover:bg-zinc-800 disabled:opacity-30"
            >
              <ChevronLeft size={14} />
            </button>
            <button
              onClick={() => setPage(p => Math.min(totalPages, p + 1))}
              disabled={page === totalPages}
              className="rounded p-1 hover:bg-zinc-800 disabled:opacity-30"
            >
              <ChevronRight size={14} />
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
