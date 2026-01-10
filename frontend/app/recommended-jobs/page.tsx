"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import JobCard from "@/components/JobCard";
import { searchRecommendedJobs } from "@/lib/hybridJobsApi";

export default function RecommendedJobsPage() {
    const [jobs, setJobs] = useState<any[]>([]);
    const [externalLinks, setExternalLinks] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [sortBy, setSortBy] = useState("match");
    const [page, setPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const router = useRouter();

    useEffect(() => {
        fetchRecommendations(1);
    }, [sortBy]);

    const fetchRecommendations = async (newPage: number) => {
        setLoading(true);
        setError("");
        setPage(newPage);
        setPage(newPage);
        window.scrollTo({ top: 0, behavior: "smooth" });
        try {
            const token = localStorage.getItem("token");
            if (!token) {
                router.push("/login");
                return;
            }

            const res = await searchRecommendedJobs(token, newPage, 10);

            setJobs(res.jobs);
            setExternalLinks(res.external_search_links);
            setTotalPages(Math.ceil(res.total / 10) || 1);
        } catch (err: any) {
            console.error(err);
            if (err.response?.status === 401) {
                router.push("/login");
            } else {
                setError("Failed to fetch recommendations. Please try again.");
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gray-100 p-8">
            <div className="max-w-6xl mx-auto">
                <div className="flex justify-between items-center mb-8">
                    <h1 className="text-3xl font-bold text-gray-900">Recommended for You</h1>

                    <div className="flex items-center space-x-2">
                        <label className="text-sm font-medium text-gray-700">Sort by:</label>
                        <select
                            value={sortBy}
                            onChange={(e) => setSortBy(e.target.value)}
                            className="px-3 py-2 border rounded-md bg-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                        >
                            <option value="match">Best Match</option>
                            <option value="latest">Latest</option>
                            <option value="salary">Highest Salary</option>
                        </select>
                    </div>
                </div>

                {/* External Search Links */}
                {externalLinks && (
                    <div className="mb-8 bg-white p-6 rounded-lg shadow-sm border border-gray-200">
                        <h3 className="text-lg font-semibold text-gray-900 mb-4">Search Externally</h3>
                        <div className="flex flex-wrap gap-4">
                            <a href={externalLinks.linkedin} target="_blank" rel="noopener noreferrer" className="px-4 py-2 bg-[#0077b5] text-white rounded-md hover:opacity-90 transition-opacity flex items-center gap-2">
                                <span>LinkedIn Jobs</span>
                            </a>
                            <a href={externalLinks.indeed} target="_blank" rel="noopener noreferrer" className="px-4 py-2 bg-[#2164f3] text-white rounded-md hover:opacity-90 transition-opacity flex items-center gap-2">
                                <span>Indeed Jobs</span>
                            </a>
                            <a href={externalLinks.google_jobs} target="_blank" rel="noopener noreferrer" className="px-4 py-2 bg-white text-gray-800 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors flex items-center gap-2">
                                <span>Google Jobs</span>
                            </a>
                        </div>
                    </div>
                )}

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

                {error && <div className="p-4 mb-6 bg-red-100 text-red-700 rounded-md">{error}</div>}

                {!loading && jobs.length === 0 && !error && (
                    <div className="text-center text-gray-600 py-10 bg-white rounded-lg shadow-sm">
                        <div className="text-4xl mb-4">📋</div>
                        <h3 className="text-xl font-semibold text-gray-900 mb-2">No Recommendations Yet</h3>
                        <p className="text-gray-500 max-w-md mx-auto">
                            We need more data to recommend jobs. Please upload your resume and search for some jobs first.
                        </p>
                        <div className="mt-6 space-x-4">
                            <button
                                onClick={() => router.push("/upload-resume")}
                                className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
                            >
                                Upload Resume
                            </button>
                            <button
                                onClick={() => router.push("/jobs")}
                                className="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300"
                            >
                                Search Jobs
                            </button>
                        </div>
                    </div>
                )}

                <div className="grid gap-6 md:grid-cols-1">
                    {jobs.map((job, index) => (
                        <JobCard key={index} job={job} />
                    ))}
                </div>

                {/* Pagination Controls */}
                {!loading && jobs.length > 0 && totalPages > 1 && (
                    <div className="flex justify-center mt-8 space-x-4">
                        <button
                            onClick={() => fetchRecommendations(page - 1)}
                            disabled={page === 1}
                            className="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            Previous
                        </button>
                        <span className="px-4 py-2 text-gray-700">
                            Page {page} of {totalPages}
                        </span>
                        <button
                            onClick={() => fetchRecommendations(page + 1)}
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
