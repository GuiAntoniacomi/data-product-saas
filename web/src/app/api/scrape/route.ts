import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'
import { spawn } from 'child_process'
import path from 'path'

export async function POST(request: Request) {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })

  const body = await request.json().catch(() => ({}))
  const categories: string[] | undefined = body.categories

  // Cria o job no Supabase
  const { data: job, error } = await supabase
    .from('ts_scraper_jobs')
    .insert({ status: 'pending', categories: categories ?? null })
    .select()
    .single()

  if (error || !job) {
    return NextResponse.json({ error: 'Falha ao criar job' }, { status: 500 })
  }

  // Spawn do Python em background (não bloqueia a response)
  const scraperDir = path.resolve(process.cwd(), '..', 'scraper')
  const args = ['main.py', '--job-id', job.id]
  if (categories?.length) args.push('--categories', categories.join(','))

  const child = spawn('python', args, {
    cwd: scraperDir,
    detached: true,
    stdio: 'ignore',
    env: {
      ...process.env,
      SUPABASE_URL: process.env.NEXT_PUBLIC_SUPABASE_URL,
      SUPABASE_SERVICE_ROLE_KEY: process.env.SUPABASE_SERVICE_ROLE_KEY,
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
    .order('created_at', { ascending: false })
    .limit(10)

  return NextResponse.json({ jobs: data ?? [] })
}
