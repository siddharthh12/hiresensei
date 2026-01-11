import { useState, useEffect } from "react";
import { saveJob, markApplied, markNotInterested, getJobStatus } from "@/lib/trackingApi";

interface JobCardProps {
    job: any;
    onStatusChange?: () => void;
}

export default function JobCard({ job, onStatusChange }: JobCardProps) {
    const [status, setStatus] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        // If job has status from backend (e.g. in tracking list), use it
        if (job.status) {
            setStatus(job.status);
        } else {
            // Otherwise fetch it (e.g. in search results)
            checkStatus();
        }
    }, [job.job_id]);

    const checkStatus = async () => {
        try {
            const res = await getJobStatus(job.job_id);
            setStatus(res.data.status);
        } catch (err) {
            console.error("Failed to check status", err);
        }
    };

    const handleAction = async (action: "save" | "apply" | "not_interested") => {
        setLoading(true);
        try {
            if (action === "save") {
                await saveJob(job);
                setStatus("saved");
            } else if (action === "apply") {
                await markApplied(job);
                setStatus("applied");
                if (job.apply_link) {
                    window.open(job.apply_link, "_blank");
                }
            } else if (action === "not_interested") {
                await markNotInterested(job);
                setStatus("not_interested");
            }
            if (onStatusChange) onStatusChange();
        } catch (err) {
            console.error(`Failed to ${action} job`, err);
        } finally {
            setLoading(false);
        }
    };

    if (status === "not_interested" && !onStatusChange) {
        // In search results, maybe dim it or hide it?
        return (
            <div className="bg-gray-50 p-4 rounded-lg border border-gray-200 opacity-50">
                <div className="flex justify-between items-center">
                    <h3 className="text-gray-500 font-medium">{job.title}</h3>
                    <span className="text-xs text-gray-400">Not Interested</span>
                </div>
            </div>
        );
    }

    return (
        <div className={`bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow border border-gray-100 relative ${status === 'saved' ? 'border-l-4 border-l-yellow-400' : status === 'applied' ? 'border-l-4 border-l-green-500' : ''}`}>
            <div className="flex justify-between items-start">
                <div className="flex-1">
                    <div className="flex flex-wrap items-center gap-3 mb-1">
                        <h2 className="text-xl font-bold text-gray-900 break-words">{job.title}</h2>
                        {job.match_score && (
                            <span className={`px-2 py-0.5 rounded text-xs font-semibold ${job.match_score >= 80 ? 'bg-green-100 text-green-800' :
                                job.match_score >= 50 ? 'bg-yellow-100 text-yellow-800' :
                                    'bg-gray-100 text-gray-800'
                                }`}>
                                {job.match_score}% Match
                            </span>
                        )}
                        {status === "saved" && <span className="text-yellow-500 text-lg">⭐</span>}
                        {status === "applied" && <span className="text-green-500 text-lg">✅</span>}
                    </div>
                    <p className="text-lg text-gray-700 font-medium mb-2">{job.company}</p>

                    <div className="flex flex-wrap gap-2 text-sm text-gray-600 mb-4">
                        <span className="bg-gray-100 px-3 py-1 rounded-full flex items-center">
                            📍 {job.location || "Remote"}
                        </span>
                        {job.job_type && (
                            <span className="bg-primary-50 text-primary-700 px-3 py-1 rounded-full">
                                💼 {job.job_type}
                            </span>
                        )}
                        {job.posted_date && (
                            <span className="bg-green-50 text-green-700 px-3 py-1 rounded-full">
                                📅 {new Date(job.posted_date).toLocaleDateString()}
                            </span>
                        )}
                        {/* Source Badge */}
                        {job.source && (
                            <span className={`px-3 py-1 rounded-full text-xs font-semibold ${job.source === 'api' ? 'bg-blue-100 text-blue-800' :
                                job.source === 'remoteok' ? 'bg-green-100 text-green-800' :
                                    job.source === 'wwr' ? 'bg-orange-100 text-orange-800' :
                                        job.source === 'hn' ? 'bg-gray-100 text-gray-800' :
                                            'bg-gray-100 text-gray-800'
                                }`}>
                                🏷️ {job.source === 'api' ? 'JSearch' :
                                    job.source === 'wwr' ? 'WeWorkRemotely' :
                                        job.source === 'hn' ? 'HackerNews' :
                                            job.source === 'remoteok' ? 'RemoteOK' : job.source}
                            </span>
                        )}
                    </div>
                    <p className="text-gray-600 line-clamp-3 mb-4">{job.description}</p>

                    {/* Explanation Panel (if available) */}
                    {job.reason && (
                        <div className="mb-4 bg-primary-50 p-3 rounded-md border border-primary-100 text-sm">
                            <p className="text-primary-800 font-medium mb-1">💡 Why this job?</p>
                            <p className="text-primary-700">{job.reason}</p>
                            {job.matching_skills && job.matching_skills.length > 0 && (
                                <div className="mt-2">
                                    <p className="text-primary-800 font-medium mb-1">✅ Matching Skills:</p>
                                    <div className="flex flex-wrap gap-1">
                                        {job.matching_skills.map((skill: string, idx: number) => (
                                            <span key={idx} className="bg-primary-100 text-primary-700 px-2 py-0.5 rounded text-xs">
                                                {skill}
                                            </span>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            </div>

            <div className="flex flex-col sm:flex-row flex-wrap gap-3 mt-4 pt-4 border-t border-gray-100">
                <div className="flex gap-3 w-full sm:w-auto">
                    <button
                        onClick={() => handleAction("save")}
                        disabled={loading || status === "saved"}
                        className={`flex-1 sm:flex-none px-4 py-2 rounded-md text-sm font-medium transition-colors ${status === "saved"
                            ? "bg-yellow-100 text-yellow-700 cursor-default"
                            : "bg-white border border-gray-300 text-gray-700 hover:bg-gray-50"
                            }`}
                    >
                        {status === "saved" ? "Saved" : "Save"}
                    </button>

                    <button
                        onClick={() => handleAction("apply")}
                        disabled={loading}
                        className="flex-1 sm:flex-none px-4 py-2 rounded-md text-sm font-medium transition-colors bg-primary-600 text-white hover:bg-primary-700"
                    >
                        Apply Now
                    </button>
                </div>

                {status === "applied" && (
                    <span className="px-3 py-2 text-green-600 font-medium text-sm flex items-center justify-center sm:justify-start">
                        ✅ Applied
                    </span>
                )}

                <button
                    onClick={() => handleAction("not_interested")}
                    disabled={loading || status === "not_interested"}
                    className="w-full sm:w-auto px-4 py-2 rounded-md text-sm font-medium text-gray-500 hover:text-gray-700 hover:bg-gray-100 transition-colors sm:ml-auto text-center"
                >
                    Not Interested
                </button>
            </div>
        </div>
    );
}
