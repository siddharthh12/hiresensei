'use client';

import { useState, useEffect } from 'react';
import { getSkillAnalysis } from '@/lib/skillsApi';
import { useRouter } from 'next/navigation';
import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ResponsiveContainer,
    Radar,
    RadarChart,
    PolarGrid,
    PolarAngleAxis,
    PolarRadiusAxis,
} from 'recharts';

interface SkillAnalysisData {
    user_skills: string[];
    market_skills: string[];
    missing_skills: { skill: string; priority: number; frequency: number }[];
    top_market_skills: { skill: string; frequency: number }[];
    skill_strengths: { skill: string; coverage: number }[];
    total_jobs_analyzed: number;
}

export default function SkillGapPage() {
    const [data, setData] = useState<SkillAnalysisData | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const router = useRouter();

    const fetchData = async () => {
        setLoading(true);
        setError('');
        const token = localStorage.getItem('token');
        if (!token) {
            router.push('/login');
            return;
        }

        try {
            const response = await getSkillAnalysis(token);
            setData(response.data);
        } catch (err) {
            setError('Failed to load skill analysis. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    if (loading) {
        return (
            <div className="min-h-screen bg-gray-900 text-white p-8 flex justify-center items-center">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500"></div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="min-h-screen bg-gray-900 text-white p-8 flex justify-center items-center">
                <div className="text-red-500 text-xl">{error}</div>
            </div>
        );
    }

    if (!data) return null;

    return (
        <div className="min-h-screen bg-gray-900 text-white p-8">
            <div className="max-w-7xl mx-auto">
                <div className="flex justify-between items-center mb-8">
                    <div>
                        <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary-400 to-purple-600">
                            Skill Gap Analysis
                        </h1>
                        <p className="text-gray-400 mt-2">
                            Analyzed {data.total_jobs_analyzed} jobs to find your missing opportunities.
                        </p>
                    </div>
                    <button
                        onClick={fetchData}
                        className="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg transition-colors flex items-center gap-2"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                            <path fillRule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clipRule="evenodd" />
                        </svg>
                        Recalculate
                    </button>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
                    {/* Missing Skills Section */}
                    <div className="bg-gray-800 rounded-xl p-6 border border-gray-700 shadow-lg">
                        <h2 className="text-xl font-semibold mb-4 text-red-400 flex items-center gap-2">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                            </svg>
                            Top Missing Skills
                        </h2>
                        <div className="space-y-4">
                            {data.missing_skills.slice(0, 5).map((item) => (
                                <div key={item.skill} className="bg-gray-700/50 p-4 rounded-lg">
                                    <div className="flex justify-between items-center mb-2">
                                        <span className="font-medium text-lg capitalize">{item.skill}</span>
                                        <span className="text-sm text-gray-400">{item.frequency} jobs</span>
                                    </div>
                                    <div className="w-full bg-gray-700 rounded-full h-2.5">
                                        <div
                                            className="bg-red-500 h-2.5 rounded-full transition-all duration-500"
                                            style={{ width: `${item.priority}%` }}
                                        ></div>
                                    </div>
                                    <div className="flex justify-between mt-1 text-xs text-gray-400">
                                        <span>Priority Score</span>
                                        <span>{item.priority}/100</span>
                                    </div>
                                </div>
                            ))}
                            {data.missing_skills.length === 0 && (
                                <p className="text-gray-400 text-center py-4">Great job! No major missing skills found.</p>
                            )}
                        </div>
                    </div>

                    {/* User Skills Section */}
                    <div className="bg-gray-800 rounded-xl p-6 border border-gray-700 shadow-lg">
                        <h2 className="text-xl font-semibold mb-4 text-green-400 flex items-center gap-2">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            Your Strongest Skills
                        </h2>
                        <div className="flex flex-wrap gap-2 mb-6">
                            {data.user_skills.map((skill) => (
                                <span key={skill} className="px-3 py-1 bg-green-500/20 text-green-400 rounded-full text-sm border border-green-500/30 capitalize">
                                    {skill}
                                </span>
                            ))}
                        </div>

                        <div className="h-[300px] w-full">
                            <ResponsiveContainer width="100%" height="100%">
                                <RadarChart cx="50%" cy="50%" outerRadius="80%" data={data.skill_strengths.slice(0, 6)}>
                                    <PolarGrid stroke="#374151" />
                                    <PolarAngleAxis dataKey="skill" tick={{ fill: '#9CA3AF' }} />
                                    <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                                    <Radar
                                        name="Skill Strength"
                                        dataKey="coverage"
                                        stroke="#10B981"
                                        fill="#10B981"
                                        fillOpacity={0.5}
                                    />
                                    <Tooltip
                                        contentStyle={{ backgroundColor: '#1F2937', borderColor: '#374151', color: '#fff' }}
                                        itemStyle={{ color: '#10B981' }}
                                    />
                                </RadarChart>
                            </ResponsiveContainer>
                        </div>
                    </div>
                </div>

                {/* Market Demand Chart */}
                <div className="bg-gray-800 rounded-xl p-6 border border-gray-700 shadow-lg mb-8">
                    <h2 className="text-xl font-semibold mb-6 text-primary-400">Market Demand (Top Skills)</h2>
                    <div className="h-[400px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={data.top_market_skills}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#374151" vertical={false} />
                                <XAxis dataKey="skill" tick={{ fill: '#9CA3AF' }} axisLine={false} tickLine={false} />
                                <YAxis tick={{ fill: '#9CA3AF' }} axisLine={false} tickLine={false} />
                                <Tooltip
                                    cursor={{ fill: '#374151', opacity: 0.4 }}
                                    contentStyle={{ backgroundColor: '#1F2937', borderColor: '#374151', color: '#fff' }}
                                />
                                <Bar dataKey="frequency" fill="#3D9B9D" radius={[4, 4, 0, 0]} />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Recommendations */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="bg-gradient-to-br from-red-900/40 to-gray-800 p-6 rounded-xl border border-red-500/20">
                        <h3 className="text-lg font-semibold text-red-400 mb-2">High Priority</h3>
                        <p className="text-sm text-gray-400 mb-4">Learn these immediately to boost your match score.</p>
                        <ul className="space-y-2">
                            {data.missing_skills.filter(s => s.priority >= 70).slice(0, 3).map(s => (
                                <li key={s.skill} className="flex items-center gap-2 text-gray-200 capitalize">
                                    <span className="w-2 h-2 bg-red-500 rounded-full"></span>
                                    {s.skill}
                                </li>
                            ))}
                            {data.missing_skills.filter(s => s.priority >= 70).length === 0 && (
                                <li className="text-gray-500 italic">None</li>
                            )}
                        </ul>
                    </div>

                    <div className="bg-gradient-to-br from-yellow-900/40 to-gray-800 p-6 rounded-xl border border-yellow-500/20">
                        <h3 className="text-lg font-semibold text-yellow-400 mb-2">Medium Priority</h3>
                        <p className="text-sm text-gray-400 mb-4">Good to have skills that appear frequently.</p>
                        <ul className="space-y-2">
                            {data.missing_skills.filter(s => s.priority >= 40 && s.priority < 70).slice(0, 3).map(s => (
                                <li key={s.skill} className="flex items-center gap-2 text-gray-200 capitalize">
                                    <span className="w-2 h-2 bg-yellow-500 rounded-full"></span>
                                    {s.skill}
                                </li>
                            ))}
                            {data.missing_skills.filter(s => s.priority >= 40 && s.priority < 70).length === 0 && (
                                <li className="text-gray-500 italic">None</li>
                            )}
                        </ul>
                    </div>

                    <div className="bg-gradient-to-br from-primary-900/40 to-gray-800 p-6 rounded-xl border border-primary-500/20">
                        <h3 className="text-lg font-semibold text-primary-400 mb-2">Low Priority</h3>
                        <p className="text-sm text-gray-400 mb-4">Niche skills that can set you apart.</p>
                        <ul className="space-y-2">
                            {data.missing_skills.filter(s => s.priority < 40).slice(0, 3).map(s => (
                                <li key={s.skill} className="flex items-center gap-2 text-gray-200 capitalize">
                                    <span className="w-2 h-2 bg-primary-500 rounded-full"></span>
                                    {s.skill}
                                </li>
                            ))}
                            {data.missing_skills.filter(s => s.priority < 40).length === 0 && (
                                <li className="text-gray-500 italic">None</li>
                            )}
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    );
}
