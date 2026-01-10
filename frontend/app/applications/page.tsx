"use client";

import { useState, useEffect } from "react";
import { getTrackedJobs } from "@/lib/trackingApi";
import ApplicationCard from "@/components/ApplicationCard";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function ApplicationsPage() {
    const [jobs, setJobs] = useState<any[]>([]);
    const [activeTab, setActiveTab] = useState("saved");
    const [loading, setLoading] = useState(true);
    const [page, setPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const [totalCount, setTotalCount] = useState(0);

    const router = useRouter();

    useEffect(() => {
        fetchTrackedJobs();
    }, [activeTab, page]);

    const fetchTrackedJobs = async () => {
        setLoading(true);
        try {
            const token = localStorage.getItem("token");
            if (!token) {
                router.push("/login");
                return;
            }
            const res = await getTrackedJobs(activeTab, page, 9);
            setJobs(res.data.data);
            setTotalPages(res.data.total_pages);
            setTotalCount(res.data.total);
        } catch (err) {
            console.error("Failed to fetch tracked jobs", err);
        } finally {
            setLoading(false);
        }
    };

    const handleTabChange = (tab: string) => {
        setActiveTab(tab);
        setPage(1); // Reset to first page when switching tabs
    };

    const handlePageChange = (newPage: number) => {
        if (newPage >= 1 && newPage <= totalPages) {
            setPage(newPage);
            window.scrollTo({ top: 0, behavior: "smooth" });
        }
    };

    return (
        <div className="min-h-screen bg-gray-900 pb-20 text-white">
            {/* Header / Banner */}
            <div className="bg-gray-900 border-b border-gray-800 py-12 px-6 sm:px-8">
                <div className="max-w-7xl mx-auto">
                    <h1 className="text-4xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-primary-400 to-purple-600 tracking-tight">
                        My Applications
                    </h1>
                    <p className="mt-3 text-lg text-gray-400 max-w-2xl">
                        Track and manage your job search journey properly.
                    </p>
                </div>
            </div>

            <div className="max-w-7xl mx-auto px-6 sm:px-8 mt-8">
                {/* Tabs */}
                <div className="flex flex-wrap items-center gap-2 mb-8 bg-gray-800 p-1.5 rounded-xl border border-gray-700 shadow-sm w-fit">
                    {["saved", "applied", "not_interested"].map((tab) => (
                        <button
                            key={tab}
                            onClick={() => handleTabChange(tab)}
                            className={`px-5 py-2.5 rounded-lg text-sm font-semibold transition-all duration-200 capitalize flex items-center gap-2 ${activeTab === tab
                                ? "bg-gray-700 text-white shadow-md transform scale-105"
                                : "text-gray-400 hover:text-white hover:bg-gray-700/50"
                                }`}
                        >
                            {tab.replace("_", " ")}
                            {activeTab === tab && (
                                <span className="bg-gray-600 px-2 py-0.5 rounded text-xs text-gray-200">
                                    {totalCount}
                                </span>
                            )}
                        </button>
                    ))}
                </div>

                {/* Content */}
                {loading ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-pulse">
                        {[...Array(6)].map((_, i) => (
                            <div key={i} className="h-64 bg-gray-800 rounded-xl border border-gray-700"></div>
                        ))}
                    </div>
                ) : jobs.length === 0 ? (
                    <div className="text-center py-24 bg-gray-800 rounded-2xl border border-dashed border-gray-700">
                        <div className="text-5xl mb-4">📭</div>
                        <h3 className="text-xl font-medium text-gray-200 mb-2">No jobs found in {activeTab.replace("_", " ")}</h3>
                        <p className="text-gray-400 mb-6">Start exploring jobs and add them to your tracker.</p>
                        <Link
                            href="/jobs"
                            className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                        >
                            Explore Jobs
                        </Link>
                    </div>
                ) : (
                    <>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
                            {jobs.map((job: any) => (
                                <ApplicationCard key={job.job_id} job={job} />
                            ))}
                        </div>

                        {/* Pagination */}
                        {totalPages > 1 && (
                            <div className="flex justify-center items-center gap-4">
                                <button
                                    onClick={() => handlePageChange(page - 1)}
                                    disabled={page === 1}
                                    className="px-4 py-2 border border-gray-700 rounded-md text-sm font-medium text-gray-300 bg-gray-800 hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                                >
                                    Previous
                                </button>
                                <span className="text-sm font-medium text-gray-400">
                                    Page {page} of {totalPages}
                                </span>
                                <button
                                    onClick={() => handlePageChange(page + 1)}
                                    disabled={page === totalPages}
                                    className="px-4 py-2 border border-gray-700 rounded-md text-sm font-medium text-gray-300 bg-gray-800 hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                                >
                                    Next
                                </button>
                            </div>
                        )}
                    </>
                )}
            </div>
        </div>
    );
}
