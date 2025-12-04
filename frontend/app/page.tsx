'use client';

import Link from "next/link";
import { useAuth } from "@/hooks/useAuth";

export default function Home() {
  const { isAuthenticated, loading } = useAuth();
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gray-900 text-white">
      <main className="flex flex-col items-center justify-center w-full flex-1 px-20 text-center">
        <h1 className="text-6xl font-bold mb-8">
          Welcome to{" "}
          <span className="bg-clip-text text-transparent bg-gradient-to-r from-primary-400 to-purple-600">
            HIREsensei
          </span>
        </h1>

        <p className="mt-3 text-2xl text-gray-400 max-w-2xl">
          Upload your resume, get AI-powered job recommendations, and bridge your skill gaps instantly.
        </p>

        <div className="mt-12 flex flex-wrap justify-center gap-6">
          {loading ? (
            <div className="animate-pulse h-12 w-32 bg-gray-700 rounded-full"></div>
          ) : isAuthenticated ? (
            <Link
              href="/dashboard"
              className="px-8 py-4 bg-primary-600 hover:bg-primary-700 text-white rounded-full font-bold text-lg transition-all transform hover:scale-105 shadow-lg shadow-primary-500/30"
            >
              Go to Dashboard
            </Link>
          ) : (
            <>
              <Link
                href="/login"
                className="px-8 py-4 bg-primary-600 hover:bg-primary-700 text-white rounded-full font-bold text-lg transition-all transform hover:scale-105 shadow-lg shadow-primary-500/30"
              >
                Get Started
              </Link>
              <Link
                href="/register"
                className="px-8 py-4 bg-gray-800 hover:bg-gray-700 text-white rounded-full font-bold text-lg border border-gray-700 transition-all transform hover:scale-105"
              >
                Create Account
              </Link>
            </>
          )}
        </div>

        <div className="mt-20 grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl">
          <div className="p-6 bg-gray-800 rounded-xl border border-gray-700">
            <h3 className="text-xl font-bold text-primary-400 mb-2">Resume Parsing</h3>
            <p className="text-gray-400">
              Automatically extract skills and experience from your PDF/DOCX resume.
            </p>
          </div>
          <div className="p-6 bg-gray-800 rounded-xl border border-gray-700">
            <h3 className="text-xl font-bold text-purple-400 mb-2">AI Matching</h3>
            <p className="text-gray-400">
              Get matched with jobs that fit your profile using advanced AI algorithms.
            </p>
          </div>
          <div className="p-6 bg-gray-800 rounded-xl border border-gray-700">
            <h3 className="text-xl font-bold text-green-400 mb-2">Skill Gap Analysis</h3>
            <p className="text-gray-400">
              Identify missing skills and get personalized recommendations to improve.
            </p>
          </div>
        </div>
      </main>

      <footer className="flex items-center justify-center w-full h-24 border-t border-gray-800 text-gray-500">
        Powered by Next.js & FastAPI
      </footer>
    </div>
  );
}
