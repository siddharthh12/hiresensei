'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';


export default function Navbar() {
    const { isAuthenticated, logout, loading } = useAuth();
    const pathname = usePathname();
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

    if (loading) return null; // Or a skeleton

    const isActive = (path: string) => pathname === path;

    const linkClass = (path: string) =>
        `px-3 py-2 rounded-md text-sm font-medium transition-colors block ${isActive(path)
            ? 'bg-primary-800 text-white'
            : 'text-primary-100 hover:bg-primary-700 hover:text-white'
        }`;

    const toggleMobileMenu = () => {
        setIsMobileMenuOpen(!isMobileMenuOpen);
    };

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
                                    <Link href="/" className={linkClass('/').replace('block', '')}>
                                        Home
                                    </Link>
                                    <Link href="/dashboard" className={linkClass('/dashboard').replace('block', '')}>
                                        Dashboard
                                    </Link>
                                    <Link href="/jobs" className={linkClass('/jobs').replace('block', '')}>
                                        Jobs
                                    </Link>
                                    <Link href="/recommended-jobs" className={linkClass('/recommended-jobs').replace('block', '')}>
                                        Recommended
                                    </Link>
                                    <Link href="/applications" className={linkClass('/applications').replace('block', '')}>
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
                    {/* Mobile menu button */}
                    <div className="-mr-2 flex md:hidden">
                        <button
                            onClick={toggleMobileMenu}
                            type="button"
                            className="bg-primary-800 inline-flex items-center justify-center p-2 rounded-md text-primary-400 hover:text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-primary-800 focus:ring-white"
                            aria-controls="mobile-menu"
                            aria-expanded="false"
                        >
                            <span className="sr-only">Open main menu</span>
                            {!isMobileMenuOpen ? (
                                <svg className="block h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" />
                                </svg>
                            ) : (
                                <svg className="block h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                                </svg>
                            )}
                        </button>
                    </div>
                </div>
            </div>

            {/* Mobile Menu */}
            {isMobileMenuOpen && (
                <div className="md:hidden" id="mobile-menu">
                    <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
                        {isAuthenticated && (
                            <>
                                <Link href="/" onClick={() => setIsMobileMenuOpen(false)} className={linkClass('/')}>
                                    Home
                                </Link>
                                <Link href="/dashboard" onClick={() => setIsMobileMenuOpen(false)} className={linkClass('/dashboard')}>
                                    Dashboard
                                </Link>
                                <Link href="/jobs" onClick={() => setIsMobileMenuOpen(false)} className={linkClass('/jobs')}>
                                    Jobs
                                </Link>
                                <Link href="/recommended-jobs" onClick={() => setIsMobileMenuOpen(false)} className={linkClass('/recommended-jobs')}>
                                    Recommended
                                </Link>
                                <Link href="/applications" onClick={() => setIsMobileMenuOpen(false)} className={linkClass('/applications')}>
                                    Applications
                                </Link>
                            </>
                        )}
                    </div>
                    <div className="pt-4 pb-4 border-t border-primary-700">
                        <div className="px-5 flex items-center">
                            {isAuthenticated ? (
                                <button
                                    onClick={() => {
                                        setIsMobileMenuOpen(false);
                                        logout();
                                    }}
                                    className="block w-full text-center bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
                                >
                                    Logout
                                </button>
                            ) : (
                                <div className="space-y-2">
                                    <Link
                                        href="/login"
                                        onClick={() => setIsMobileMenuOpen(false)}
                                        className="block w-full text-center text-primary-100 hover:bg-primary-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium"
                                    >
                                        Login
                                    </Link>
                                    <Link
                                        href="/register"
                                        onClick={() => setIsMobileMenuOpen(false)}
                                        className="block w-full text-center bg-primary-500 hover:bg-primary-600 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
                                    >
                                        Register
                                    </Link>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            )}
        </nav>
    );
}
