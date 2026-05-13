import { createClient } from '@/lib/supabase/server'
import { TrendTable } from './_components/trend-table'
import { TrendsButton } from '@/components/dashboard/trends-button'

export default async function TrendsPage() {
  const supabase = await createClient()

  const { data: signals } = await supabase
    .from('ts_trend_signals')
    .select('*')
    .order('opportunity_score', { ascending: false })
    .limit(200)

  return (
    <div className="p-8 space-y-6">
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Tendências Emergentes</h1>
          <p className="mt-1 text-sm text-zinc-400">
            Módulo 1B — oportunidades detectadas via Reddit e Google Trends, analisadas por LLM
          </p>
        </div>
        <TrendsButton />
      </div>

      <TrendTable signals={signals ?? []} />
    </div>
  )
}
