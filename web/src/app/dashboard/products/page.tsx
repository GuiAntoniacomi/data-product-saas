import { createClient } from '@/lib/supabase/server'
import { ProductTable } from './_components/product-table'
import { ScraperButton } from '@/components/dashboard/scraper-button'

export default async function ProductsPage() {
  const supabase = await createClient()

  const { data: products } = await supabase
    .from('ts_product_cache')
    .select('*')
    .order('score', { ascending: false })
    .limit(100)

  return (
    <div className="p-8 space-y-6">
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Descoberta de Produtos</h1>
          <p className="mt-1 text-sm text-zinc-400">
            Módulo 1A — produtos com margem calculada e score de oportunidade
          </p>
        </div>
        <ScraperButton />
      </div>

      <ProductTable products={products ?? []} />
    </div>
  )
}
