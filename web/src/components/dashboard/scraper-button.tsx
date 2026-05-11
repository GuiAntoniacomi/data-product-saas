'use client'

import { useState, useEffect, useCallback } from 'react'
import { Play, Loader2, CheckCircle2, XCircle, Clock } from 'lucide-react'
import { clsx } from 'clsx'

type JobStatus = 'idle' | 'pending' | 'running' | 'completed' | 'failed'

type Job = {
  id: string
  status: string
  products_found: number
  created_at: string
  completed_at: string | null
  error: string | null
}

export function ScraperButton({ onComplete }: { onComplete?: () => void }) {
  const [status, setStatus] = useState<JobStatus>('idle')
  const [jobId, setJobId] = useState<string | null>(null)
  const [lastJob, setLastJob] = useState<Job | null>(null)

  // Carrega último job ao montar
  useEffect(() => {
    fetch('/api/scrape')
      .then(r => r.json())
      .then(({ jobs }) => {
        if (jobs?.length) setLastJob(jobs[0])
      })
      .catch(() => null)
  }, [])

  // Polling do job ativo
  const pollJob = useCallback((id: string) => {
    const interval = setInterval(async () => {
      const res = await fetch(`/api/scrape/${id}`)
      const { job } = await res.json()
      if (!job) return

      if (job.status === 'completed') {
        clearInterval(interval)
        setStatus('completed')
        setLastJob(job)
        onComplete?.()
      } else if (job.status === 'failed') {
        clearInterval(interval)
        setStatus('failed')
        setLastJob(job)
      }
    }, 3000)
    return interval
  }, [onComplete])

  useEffect(() => {
    if (!jobId) return
    const interval = pollJob(jobId)
    return () => clearInterval(interval)
  }, [jobId, pollJob])

  async function handleRun() {
    setStatus('pending')
    try {
      const res = await fetch('/api/scrape', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}' })
      const { jobId: id } = await res.json()
      setJobId(id)
      setStatus('running')
    } catch {
      setStatus('failed')
    }
  }

  const isRunning = status === 'pending' || status === 'running'

  return (
    <div className="flex items-center gap-4">
      <button
        onClick={handleRun}
        disabled={isRunning}
        className={clsx(
          'flex items-center gap-2 rounded-md px-4 py-2 text-sm font-medium transition-colors',
          isRunning
            ? 'bg-zinc-700 text-zinc-400 cursor-not-allowed'
            : 'bg-violet-600 text-white hover:bg-violet-500'
        )}
      >
        {isRunning ? (
          <><Loader2 size={14} className="animate-spin" /> Raspando AliExpress...</>
        ) : (
          <><Play size={14} /> Executar Scraper</>
        )}
      </button>

      {status === 'completed' && (
        <span className="flex items-center gap-1.5 text-sm text-emerald-400">
          <CheckCircle2 size={14} />
          {lastJob?.products_found ?? 0} produtos encontrados
        </span>
      )}
      {status === 'failed' && (
        <span className="flex items-center gap-1.5 text-sm text-red-400">
          <XCircle size={14} /> Erro na execução
        </span>
      )}
      {status === 'idle' && lastJob && (
        <span className="flex items-center gap-1.5 text-xs text-zinc-500">
          <Clock size={12} />
          Último: {lastJob.products_found} produtos —{' '}
          {new Date(lastJob.created_at).toLocaleDateString('pt-BR')}
        </span>
      )}
    </div>
  )
}
