import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/hybrid-jobs';

export interface HybridJob {
    job_id: string;
    title: string;
    company: string;
    location: string;
    description: string;
    job_type: string;
    apply_link: string;
    source: string;
    published_at?: string;
    skills: string[];
    match_score?: number;
    matching_skills?: string[];
    missing_skills?: string[];
    experience_difference?: string;
    reason?: string;
}

export interface HybridJobResponse {
    jobs: HybridJob[];
    external_search_links: {
        linkedin: string;
        indeed: string;
        google_jobs: string;
    };
    sources_used: string[];
    total: number;
}

export const searchRecommendedJobs = async (token: string, page: number = 1, limit: number = 10): Promise<HybridJobResponse> => {
    const res = await axios.get(`${API_URL}/recommended`, {
        params: { limit, page },
        headers: { Authorization: `Bearer ${token}` }
    });
    return res.data;
};

export const searchHybridJobs = async (role: string, location: string = "", remote: boolean = false, page: number = 1, limit: number = 20): Promise<HybridJobResponse> => {
    const res = await axios.get(`${API_URL}/search`, {
        params: { role, location, remote, page, limit }
    });
    return res.data;
};
