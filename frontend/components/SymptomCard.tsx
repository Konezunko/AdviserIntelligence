"use client";

import Link from "next/link";
import { ArrowRight } from "lucide-react";

interface SymptomCardProps {
    title: string;
    description?: string;
    href: string;
    disabled?: boolean;
}

export default function SymptomCard({
    title,
    description,
    href,
    disabled = false,
}: SymptomCardProps) {
    if (disabled) {
        return (
            <div className="group relative overflow-hidden rounded-2xl border border-zinc-200 bg-zinc-100 p-6 opacity-60 dark:border-zinc-800 dark:bg-zinc-900/50">
                <div className="flex items-center justify-between">
                    <h3 className="text-lg font-semibold text-zinc-500 dark:text-zinc-400">
                        {title}
                    </h3>
                    <span className="text-xs font-medium uppercase tracking-wider text-zinc-400">
                        Coming Soon
                    </span>
                </div>
                {description && (
                    <p className="mt-2 text-sm text-zinc-400 dark:text-zinc-600">
                        {description}
                    </p>
                )}
            </div>
        );
    }

    return (
        <Link
            href={href}
            className="group relative block overflow-hidden rounded-2xl border border-zinc-200 bg-white/50 p-6 shadow-sm transition-all hover:-translate-y-1 hover:shadow-lg dark:border-zinc-800 dark:bg-zinc-900/50 dark:shadow-zinc-900/10 backdrop-blur-sm"
        >
            <div className="absolute inset-0 bg-gradient-to-br from-blue-50/50 to-purple-50/50 opacity-0 transition-opacity group-hover:opacity-100 dark:from-blue-900/10 dark:to-purple-900/10" />

            <div className="relative flex items-center justify-between">
                <div>
                    <h3 className="text-lg font-semibold text-zinc-900 dark:text-zinc-100">
                        {title}
                    </h3>
                    {description && (
                        <p className="mt-2 text-sm text-zinc-500 dark:text-zinc-400">
                            {description}
                        </p>
                    )}
                </div>
                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-zinc-100 text-zinc-900 transition-colors group-hover:bg-blue-600 group-hover:text-white dark:bg-zinc-800 dark:text-zinc-100 dark:group-hover:bg-blue-600">
                    <ArrowRight size={20} />
                </div>
            </div>
        </Link>
    );
}
