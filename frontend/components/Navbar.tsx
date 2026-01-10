'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';

export default function Navbar() {
    const { isAuthenticated, logout, loading } = useAuth();
    const pathname = usePathname();

    if (loading) return null; // Or a skeleton

    const isActive = (path: string) => pathname === path;

    const linkClass = (path: string) =>
        `px-3 py-2 rounded-md text-sm font-medium transition-colors ${isActive(path)
            ? 'bg-primary-800 text-white'
            : 'text-primary-100 hover:bg-primary-700 hover:text-white'
        }`;

    return (
        <nav className="bg-primary-900 border-b border-primary-800">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-16">
                    <div className="flex items-center">
                        <Link href="/" className="flex-shrink-0">
                            <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary-400 to-primary-200">
                                HIREsensei
                            </span>
                        </Link>
                        <div className="hidden md:block">
                            {isAuthenticated && (
                                <div className="ml-10 flex items-baseline space-x-4">
                                    <Link href="/" className={linkClass('/')}>
                                        Home
                                    </Link>
                                    <Link href="/dashboard" className={linkClass('/dashboard')}>
                                        Dashboard
                                    </Link>
                                    <Link href="/jobs" className={linkClass('/jobs')}>
                                        Jobs
                                    </Link>
                                    <Link href="/recommended-jobs" className={linkClass('/recommended-jobs')}>
                                        Recommended
                                    </Link>
                                    <Link href="/applications" className={linkClass('/applications')}>
                                        Applications
                                    </Link>

                                </div>
                            )}
                        </div>
                    </div>
                    <div className="hidden md:block">
                        <div className="ml-4 flex items-center md:ml-6">
                            {isAuthenticated ? (
                                <button
                                    onClick={logout}
                                    className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
                                >
                                    Logout
                                </button>
                            ) : (
                                <div className="space-x-4">
                                    <Link
                                        href="/login"
                                        className="text-primary-100 hover:bg-primary-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium"
                                    >
                                        Login
                                    </Link>
                                    <Link
                                        href="/register"
                                        className="bg-primary-500 hover:bg-primary-600 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
                                    >
                                        Register
                                    </Link>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </nav>
    );
}
