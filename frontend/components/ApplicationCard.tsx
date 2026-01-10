"use client";

import { motion } from "framer-motion";

interface ApplicationCardProps {
    job: any;
    onStatusChange?: () => void;
}

export default function ApplicationCard({ job }: ApplicationCardProps) {
    // Determine status color/badge
    const getStatusInfo = (status: string) => {
        switch (status) {
            case "saved": return { bg: "bg-yellow-900/30", text: "text-yellow-400", border: "border-yellow-800", label: "Saved" };
            case "applied": return { bg: "bg-green-900/30", text: "text-green-400", border: "border-green-800", label: "Applied" };
            case "not_interested": return { bg: "bg-gray-700", text: "text-gray-400", border: "border-gray-600", label: "Not Interested" };
            default: return { bg: "bg-gray-700", text: "text-gray-400", border: "border-gray-600", label: status };
        }
    };

    const statusInfo = getStatusInfo(job.status || "saved");

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className={`group bg-gray-800 rounded-xl border border-gray-700 hover:border-gray-600 shadow-sm hover:shadow-lg transition-all duration-300 overflow-hidden relative`}
        >
            {/* Gradient Top Border */}
            <div className={`h-1 w-full bg-gradient-to-r ${job.status === 'applied' ? 'from-green-400 to-emerald-500' :
                job.status === 'saved' ? 'from-yellow-400 to-amber-500' :
                    'from-gray-500 to-gray-600'
                }`} />

            <div className="p-5">
                <div className="flex justify-between items-start mb-4">
                    <div className="flex-1">
                        <h3 className="text-lg font-bold text-gray-100 group-hover:text-primary-400 transition-colors line-clamp-1">
                            {job.title}
                        </h3>
                        <p className="text-gray-400 font-medium text-sm mt-0.5">{job.company}</p>
                    </div>
                    {job.match_score && (
                        <div className={`px-2 py-1 rounded-md text-xs font-bold ${job.match_score >= 80 ? 'bg-green-900/30 text-green-400 border border-green-800' :
                            job.match_score >= 50 ? 'bg-yellow-900/30 text-yellow-400 border border-yellow-800' :
                                'bg-gray-700 text-gray-300 border border-gray-600'
                            }`}>
                            {job.match_score}%
                        </div>
                    )}
                </div>

                <div className="flex flex-wrap gap-2 mb-4">
                    <span className="inline-flex items-center text-xs text-gray-400 bg-gray-700/50 px-2 py-1 rounded-md border border-gray-700">
                        📍 {job.location || "Remote"}
                    </span>
                    <span className="inline-flex items-center text-xs text-gray-400 bg-gray-700/50 px-2 py-1 rounded-md border border-gray-700">
                        💼 {job.job_type || "Full-time"}
                    </span>
                    <span className="inline-flex items-center text-xs text-gray-400 bg-gray-700/50 px-2 py-1 rounded-md border border-gray-700">
                        🗓️ {new Date(job.posted_date || Date.now()).toLocaleDateString()}
                    </span>
                </div>

                {/* Source Badge */}
                {job.source && (
                    <div className="mb-4">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-medium uppercase tracking-wider ${job.source === 'api' ? 'bg-blue-900/30 text-blue-400 border border-blue-800' :
                            job.source === 'remoteok' ? 'bg-green-900/30 text-green-400 border border-green-800' :
                                job.source === 'wwr' ? 'bg-orange-900/30 text-orange-400 border border-orange-800' :
                                    job.source === 'hn' ? 'bg-gray-700 text-gray-300 border border-gray-600' :
                                        'bg-gray-700 text-gray-300 border border-gray-600'
                            }`}>
                            {job.source === 'api' ? 'JSearch' :
                                job.source === 'wwr' ? 'WeWorkRemotely' :
                                    job.source === 'hn' ? 'HackerNews' :
                                        job.source === 'remoteok' ? 'RemoteOK' : job.source}
                        </span>
                    </div>
                )}


                <div className="flex items-center justify-between pt-4 border-t border-gray-700">
                    <span className={`px-2.5 py-1 rounded-full text-xs font-medium border ${statusInfo.bg} ${statusInfo.text} ${statusInfo.border}`}>
                        {statusInfo.label}
                    </span>

                    <a
                        href={job.apply_link || "#"}
                        target="_blank"
                        rel="noreferrer"
                        className="text-sm font-medium text-primary-400 hover:text-primary-300 hover:underline"
                    >
                        View Details →
                    </a>
                </div>
            </div>
        </motion.div>
    );
}
