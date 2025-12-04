"use client";

import { useState } from "react";
import axios from "axios";
import JobCard from "@/components/JobCard";

export default function JobsPage() {
    const [query, setQuery] = useState("");
    const [location, setLocation] = useState("");
    const [remote, setRemote] = useState(false);
    const [jobs, setJobs] = useState<any[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [searched, setSearched] = useState(false);
    const [page, setPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);

    const handleSearch = async (e?: React.FormEvent, newPage: number = 1) => {
        if (e) e.preventDefault();
        if (!query) return;

        setPage(newPage);

        setLoading(true);
        setError("");
        setSearched(true);
        setJobs([]);

        try {
            const res = await axios.get("http://localhost:8000/job/search", {
                params: {
                    query,
                    location,
                    remote,
                    page: newPage,
                    limit: 10,
                },
            });

            if (res.data.data) {
                setJobs(res.data.data);
                setTotalPages(res.data.meta?.total_pages || 1);
            } else {
                setJobs([]);
                setTotalPages(1);
            }
        } catch (err: any) {
            console.error(err);
            setError("Failed to fetch jobs. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gray-100 p-8">
            <div className="max-w-6xl mx-auto">
                <h1 className="text-3xl font-bold text-gray-900 mb-8 text-center">Find Your Dream Job</h1>

                {/* Search Form */}
                <div className="bg-white p-6 rounded-lg shadow-md mb-8">
                    <form onSubmit={handleSearch} className="flex flex-col md:flex-row gap-4 items-end">
                        <div className="flex-1 w-full">
                            <label className="block text-sm font-medium text-gray-700 mb-1">Job Title or Skills</label>
                            <input
                                type="text"
                                value={query}
                                onChange={(e) => setQuery(e.target.value)}
                                placeholder="e.g. Python Developer"
                                className="w-full px-4 py-2 border rounded-md focus:ring-2 focus:ring-primary-500 focus:outline-none"
                                required
                            />
                        </div>
                        <div className="flex-1 w-full">
                            <label className="block text-sm font-medium text-gray-700 mb-1">Location</label>
                            <input
                                type="text"
                                value={location}
                                onChange={(e) => setLocation(e.target.value)}
                                placeholder="e.g. New York"
                                className="w-full px-4 py-2 border rounded-md focus:ring-2 focus:ring-primary-500 focus:outline-none"
                            />
                        </div>
                        <div className="flex items-center h-10 pb-2">
                            <label className="flex items-center space-x-2 cursor-pointer">
                                <input
                                    type="checkbox"
                                    checked={remote}
                                    onChange={(e) => setRemote(e.target.checked)}
                                    className="w-5 h-5 text-primary-600 rounded focus:ring-primary-500"
                                />
                                <span className="text-gray-700">Remote Only</span>
                            </label>
                        </div>
                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full md:w-auto px-6 py-2 bg-primary-600 text-white font-semibold rounded-md hover:bg-primary-700 disabled:bg-primary-400 transition-colors h-10"
                        >
                            {loading ? "Searching..." : "Search Jobs"}
                        </button>
                    </form>
                </div>

                {/* Results */}
                {error && <div className="p-4 mb-6 bg-red-100 text-red-700 rounded-md">{error}</div>}

                {loading && (
                    <div className="space-y-4">
                        {[1, 2, 3].map((i) => (
                            <div key={i} className="bg-white p-6 rounded-lg shadow-md animate-pulse">
                                <div className="h-6 bg-gray-200 rounded w-1/3 mb-4"></div>
                                <div className="h-4 bg-gray-200 rounded w-1/4 mb-2"></div>
                                <div className="h-4 bg-gray-200 rounded w-1/2"></div>
                            </div>
                        ))}
                    </div>
                )}

                {!loading && searched && jobs.length === 0 && !error && (
                    <div className="text-center text-gray-600 py-10 bg-white rounded-lg shadow-sm border border-gray-200">
                        <div className="text-4xl mb-4">🔍</div>
                        <h3 className="text-xl font-semibold text-gray-900 mb-2">No Jobs Found</h3>
                        <p className="text-gray-500 max-w-md mx-auto">
                            We couldn't find any jobs matching your criteria. Please try different keywords, location, or check back later.
                        </p>
                    </div>
                )}

                {!loading && !searched && (
                    <div className="text-center text-gray-600 py-16 bg-white rounded-lg shadow-sm border border-gray-200">
                        <div className="text-6xl mb-6">💼</div>
                        <h3 className="text-2xl font-bold text-gray-900 mb-3">Ready to Find Your Next Job?</h3>
                        <p className="text-gray-500 max-w-lg mx-auto text-lg">
                            Enter your skills, job title, or location above to start searching through our database of opportunities.
                        </p>
                    </div>
                )}

                <div className="grid gap-6 md:grid-cols-1 lg:grid-cols-1">
                    {jobs.map((job, index) => (
                        <JobCard key={index} job={job} />
                    ))}
                </div>

                {/* Pagination Controls */}
                {!loading && jobs.length > 0 && totalPages > 1 && (
                    <div className="flex justify-center mt-8 space-x-4">
                        <button
                            onClick={() => handleSearch(undefined, page - 1)}
                            disabled={page === 1}
                            className="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            Previous
                        </button>
                        <span className="px-4 py-2 text-gray-700">
                            Page {page} of {totalPages}
                        </span>
                        <button
                            onClick={() => handleSearch(undefined, page + 1)}
                            disabled={page === totalPages}
                            className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            Next
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
}
