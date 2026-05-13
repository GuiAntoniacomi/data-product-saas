import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'
import { spawn } from 'child_process'
import path from 'path'

export async function POST(request: Request) {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })

  const body = await request.json().catch(() => ({}))
  const sources: string[] | undefined = body.sources

  const { data: job, error } = await supabase
    .from('ts_scraper_jobs')
    .insert({ status: 'pending', categories: sources ?? null, job_type: 'trends' })
    .select()
    .single()

  if (error || !job) {
    return NextResponse.json({ error: 'Falha ao criar job' }, { status: 500 })
  }

  const scraperDir = path.resolve(process.cwd(), '..', 'scraper')
  const args = ['trends_main.py', '--job-id', job.id]
  if (sources?.length) args.push('--sources', sources.join(','))

  const child = spawn('python', args, {
    cwd: scraperDir,
    detached: true,
    stdio: 'ignore',
    env: {
      ...process.env,
      SUPABASE_URL: process.env.NEXT_PUBLIC_SUPABASE_URL,
      SUPABASE_SERVICE_ROLE_KEY: process.env.SUPABASE_SERVICE_ROLE_KEY,
      ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY,
      PYTHONIOENCODING: 'utf-8',
      PYTHONUTF8: '1',
    },
  })
  child.unref()

  return NextResponse.json({ jobId: job.id })
}

export async function GET() {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })

  const { data } = await supabase
    .from('ts_scraper_jobs')
    .select('*')
    .eq('job_type', 'trends')
    .order('created_at', { ascending: false })
    .limit(10)

  return NextResponse.json({ jobs: data ?? [] })
}
