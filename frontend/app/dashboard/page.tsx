'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { getDashboardSummary, getSkillAnalytics } from '@/lib/dashboardApi';
import { useAuth } from '@/hooks/useAuth';
import axios from 'axios';

interface DashboardData {
    stats: {
        recommended: number;
        saved: number;
        applied: number;
        not_interested: number;
    };
    profile: {
        skills_count: number;
        experience_years: number;
        profile_completion: number;
    };
    recent_activity: {
        saved_jobs: any[];
        applied_jobs: any[];
    };
}

interface SkillData {
    top_user_skills: string[];
    missing_skills: string[];
    recommended_skills: { skill: string; frequency: number }[];
}

export default function Dashboard() {
    const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
    const [skillData, setSkillData] = useState<SkillData | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const router = useRouter();
    const { logout } = useAuth();

    useEffect(() => {
        const fetchData = async () => {
            const token = localStorage.getItem('token');
            if (!token) {
                router.push('/login');
                return;
            }

            try {
                const [summary, skills] = await Promise.all([
                    getDashboardSummary(token),
                    getSkillAnalytics(token),
                ]);
                setDashboardData(summary);
                setSkillData(skills);

                // Redirect if no resume (simple check: completion is 0 or no skills)
                if (summary.profile.profile_completion === 0 && summary.profile.skills_count === 0) {
                    router.push('/upload-resume');
                }
            } catch (err: any) {
                if (axios.isAxiosError(err) && err.response?.status === 401) {
                    logout();
                    return;
                }
                setError('Failed to load dashboard data');
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [router]);

    if (loading) {
        return (
            <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500"></div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
                <div className="text-red-500">{error}</div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-900 text-white p-8">
            <div className="max-w-7xl mx-auto space-y-8">
                <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary-400 to-purple-600">
                    Dashboard
                </h1>

                {/* Top Section: Profile & Stats */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    {/* Profile Overview Card */}
                    <div className="bg-gray-800 rounded-xl p-6 border border-gray-700 shadow-lg">
                        <h2 className="text-xl font-semibold mb-4 text-gray-200">Profile Overview</h2>
                        <div className="space-y-4">
                            <div>
                                <div className="flex justify-between mb-1">
                                    <span className="text-sm font-medium text-gray-400">Completion</span>
                                    <span className="text-sm font-medium text-primary-400">
                                        {dashboardData?.profile.profile_completion}%
                                    </span>
                                </div>
                                <div className="w-full bg-gray-700 rounded-full h-2.5">
                                    <div
                                        className="bg-primary-600 h-2.5 rounded-full transition-all duration-500"
                                        style={{ width: `${dashboardData?.profile.profile_completion}%` }}
                                    ></div>
                                </div>
                            </div>
                            <div className="grid grid-cols-2 gap-4 mt-4">
                                <div className="bg-gray-700/50 p-3 rounded-lg text-center">
                                    <div className="text-2xl font-bold text-white">
                                        {dashboardData?.profile.skills_count}
                                    </div>
                                    <div className="text-xs text-gray-400">Skills</div>
                                </div>
                                <div className="bg-gray-700/50 p-3 rounded-lg text-center">
                                    <div className="text-2xl font-bold text-white">
                                        {dashboardData?.profile.experience_years}
                                    </div>
                                    <div className="text-xs text-gray-400">Exp. Years</div>
                                </div>
                            </div>
                            <button
                                onClick={() => router.push('/upload-resume')}
                                className="w-full mt-4 bg-gray-700 hover:bg-gray-600 text-white py-2 rounded-lg transition-colors text-sm font-medium"
                            >
                                Update Resume
                            </button>
                        </div>
                    </div>

                    {/* Job Stats Cards */}
                    <div className="lg:col-span-2 grid grid-cols-2 md:grid-cols-4 gap-4">
                        <StatCard
                            label="Recommended"
                            value={dashboardData?.stats.recommended || 0}
                            color="blue"
                        />
                        <StatCard
                            label="Saved"
                            value={dashboardData?.stats.saved || 0}
                            color="purple"
                        />
                        <StatCard
                            label="Applied"
                            value={dashboardData?.stats.applied || 0}
                            color="green"
                        />
                        <StatCard
                            label="Not Interested"
                            value={dashboardData?.stats.not_interested || 0}
                            color="red"
                        />
                    </div>
                </div>

                {/* Middle Section: Skill Insights */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="bg-gray-800 rounded-xl p-6 border border-gray-700 shadow-lg">
                        <h2 className="text-xl font-semibold mb-4 text-gray-200">Your Top Skills</h2>
                        <div className="flex flex-wrap gap-2">
                            {skillData?.top_user_skills.map((skill, idx) => (
                                <span
                                    key={idx}
                                    className="px-3 py-1 bg-primary-900/30 text-primary-400 rounded-full text-sm border border-primary-800"
                                >
                                    {skill}
                                </span>
                            ))}
                            {skillData?.top_user_skills.length === 0 && (
                                <span className="text-gray-500 text-sm">No skills found. Upload resume to see insights.</span>
                            )}
                        </div>
                    </div>

                    <div className="bg-gray-800 rounded-xl p-6 border border-gray-700 shadow-lg">
                        <h2 className="text-xl font-semibold mb-4 text-gray-200">Missing Market Skills</h2>
                        <div className="flex flex-wrap gap-2">
                            {skillData?.missing_skills.map((skill, idx) => (
                                <span
                                    key={idx}
                                    className="px-3 py-1 bg-red-900/30 text-red-400 rounded-full text-sm border border-red-800"
                                >
                                    {skill}
                                </span>
                            ))}
                            {skillData?.missing_skills.length === 0 && (
                                <span className="text-gray-500 text-sm">Great job! You match most market skills.</span>
                            )}
                        </div>
                    </div>
                </div>

                {/* Bottom Section: Recent Activity */}
                <div className="bg-gray-800 rounded-xl p-6 border border-gray-700 shadow-lg">
                    <h2 className="text-xl font-semibold mb-6 text-gray-200">Recent Activity</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                        {/* Recently Saved */}
                        <div>
                            <h3 className="text-sm font-medium text-gray-400 mb-3 uppercase tracking-wider">Recently Saved</h3>
                            <div className="space-y-3">
                                {dashboardData?.recent_activity.saved_jobs.map((job) => (
                                    <ActivityItem key={job.id} job={job} type="saved" />
                                ))}
                                {dashboardData?.recent_activity.saved_jobs.length === 0 && (
                                    <div className="text-gray-500 text-sm italic">No saved jobs yet.</div>
                                )}
                            </div>
                        </div>

                        {/* Recently Applied */}
                        <div>
                            <h3 className="text-sm font-medium text-gray-400 mb-3 uppercase tracking-wider">Recently Applied</h3>
                            <div className="space-y-3">
                                {dashboardData?.recent_activity.applied_jobs.map((job) => (
                                    <ActivityItem key={job.id} job={job} type="applied" />
                                ))}
                                {dashboardData?.recent_activity.applied_jobs.length === 0 && (
                                    <div className="text-gray-500 text-sm italic">No applied jobs yet.</div>
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

function StatCard({ label, value, color }: { label: string; value: number; color: string }) {
    const colorClasses = {
        blue: 'bg-primary-900/20 text-primary-400 border-primary-800',
        purple: 'bg-purple-900/20 text-purple-400 border-purple-800',
        green: 'bg-green-900/20 text-green-400 border-green-800',
        red: 'bg-red-900/20 text-red-400 border-red-800',
    };

    return (
        <div className={`rounded-xl p-6 border ${colorClasses[color as keyof typeof colorClasses]} flex flex-col items-center justify-center`}>
            <div className="text-3xl font-bold mb-1">{value}</div>
            <div className="text-sm font-medium opacity-80">{label}</div>
        </div>
    );
}

function ActivityItem({ job, type }: { job: any; type: 'saved' | 'applied' }) {
    return (
        <div className="flex items-center justify-between p-3 bg-gray-700/30 rounded-lg hover:bg-gray-700/50 transition-colors">
            <div>
                <div className="font-medium text-white text-sm">{job.title}</div>
                <div className="text-xs text-gray-400">{job.company}</div>
            </div>
            <div className="text-xs text-gray-500">
                {new Date(job.updated_at).toLocaleDateString()}
            </div>
        </div>
    );
}
