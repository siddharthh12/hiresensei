"use client";

import { useState, useEffect } from "react";
import { getAllTrackedJobs } from "@/lib/trackingApi";
import JobCard from "@/components/JobCard";
import { useRouter } from "next/navigation";

export default function ApplicationsPage() {
    const [trackedJobs, setTrackedJobs] = useState<any>({ saved: [], applied: [], not_interested: [] });
    const [loading, setLoading] = useState(true);
    const router = useRouter();

    useEffect(() => {
        fetchTrackedJobs();
    }, []);

    const fetchTrackedJobs = async () => {
        setLoading(true);
        try {
            const token = localStorage.getItem("token");
            if (!token) {
                router.push("/login");
                return;
            }
            const res = await getAllTrackedJobs();
            setTrackedJobs(res.data);
        } catch (err) {
            console.error("Failed to fetch tracked jobs", err);
        } finally {
            setLoading(false);
        }
    };

    const handleStatusChange = () => {
        fetchTrackedJobs();
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-gray-100 p-8 flex justify-center items-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-100 p-8">
            <div className="max-w-7xl mx-auto">
                <h1 className="text-3xl font-bold text-gray-900 mb-8">My Applications</h1>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {/* Saved Column */}
                    <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
                        <div className="flex items-center justify-between mb-4">
                            <h2 className="text-lg font-semibold text-gray-800">Saved</h2>
                            <span className="bg-yellow-100 text-yellow-800 text-xs font-bold px-2 py-1 rounded-full">
                                {trackedJobs.saved.length}
                            </span>
                        </div>
                        <div className="space-y-4">
                            {trackedJobs.saved.length === 0 ? (
                                <p className="text-gray-500 text-sm text-center py-8">No saved jobs yet.</p>
                            ) : (
                                trackedJobs.saved.map((job: any) => (
                                    <JobCard key={job.job_id} job={job} onStatusChange={handleStatusChange} />
                                ))
                            )}
                        </div>
                    </div>

                    {/* Applied Column */}
                    <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
                        <div className="flex items-center justify-between mb-4">
                            <h2 className="text-lg font-semibold text-gray-800">Applied</h2>
                            <span className="bg-green-100 text-green-800 text-xs font-bold px-2 py-1 rounded-full">
                                {trackedJobs.applied.length}
                            </span>
                        </div>
                        <div className="space-y-4">
                            {trackedJobs.applied.length === 0 ? (
                                <p className="text-gray-500 text-sm text-center py-8">No applied jobs yet.</p>
                            ) : (
                                trackedJobs.applied.map((job: any) => (
                                    <JobCard key={job.job_id} job={job} onStatusChange={handleStatusChange} />
                                ))
                            )}
                        </div>
                    </div>

                    {/* Not Interested Column */}
                    <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
                        <div className="flex items-center justify-between mb-4">
                            <h2 className="text-lg font-semibold text-gray-800">Not Interested</h2>
                            <span className="bg-gray-200 text-gray-700 text-xs font-bold px-2 py-1 rounded-full">
                                {trackedJobs.not_interested.length}
                            </span>
                        </div>
                        <div className="space-y-4">
                            {trackedJobs.not_interested.length === 0 ? (
                                <p className="text-gray-500 text-sm text-center py-8">No jobs marked as not interested.</p>
                            ) : (
                                trackedJobs.not_interested.map((job: any) => (
                                    <JobCard key={job.job_id} job={job} onStatusChange={handleStatusChange} />
                                ))
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
