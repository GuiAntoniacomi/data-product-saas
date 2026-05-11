'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { BarChart2, Search, TrendingUp, ShoppingCart, LayoutDashboard } from 'lucide-react'
import { clsx } from 'clsx'

const navItems = [
  { href: '/dashboard', label: 'Visão Geral', icon: LayoutDashboard },
  { href: '/dashboard/products', label: 'Descoberta 1A', icon: Search },
  { href: '/dashboard/trends', label: 'Tendências 1B', icon: TrendingUp },
  { href: '/dashboard/listings', label: 'Listings', icon: ShoppingCart },
  { href: '/dashboard/performance', label: 'Performance', icon: BarChart2 },
]

export function Sidebar() {
  const pathname = usePathname()

  return (
    <aside className="w-56 min-h-screen bg-zinc-950 border-r border-zinc-800 flex flex-col">
      <div className="px-4 py-5 border-b border-zinc-800">
        <span className="text-lg font-bold text-white">Vantis</span>
        <span className="ml-2 text-xs text-violet-400 font-medium">beta</span>
      </div>

      <nav className="flex-1 p-3 space-y-1">
        {navItems.map(({ href, label, icon: Icon }) => (
          <Link
            key={href}
            href={href}
            className={clsx(
              'flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors',
              pathname === href
                ? 'bg-violet-600/20 text-violet-300'
                : 'text-zinc-400 hover:bg-zinc-800 hover:text-zinc-100'
            )}
          >
            <Icon size={16} />
            {label}
          </Link>
        ))}
      </nav>

      <div className="p-3 border-t border-zinc-800">
        <p className="text-xs text-zinc-600 px-3">Você é o único usuário por enquanto</p>
      </div>
    </aside>
  )
}
