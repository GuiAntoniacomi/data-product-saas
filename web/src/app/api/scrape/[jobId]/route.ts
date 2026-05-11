import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'

export async function GET(_req: Request, ctx: RouteContext<'/api/scrape/[jobId]'>) {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })

  const { jobId } = await ctx.params
  const { data: job } = await supabase
    .from('ts_scraper_jobs')
    .select('*')
    .eq('id', jobId)
    .single()

  if (!job) return NextResponse.json({ error: 'Job não encontrado' }, { status: 404 })

  return NextResponse.json({ job })
}
