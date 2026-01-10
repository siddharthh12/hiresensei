import axios from "axios";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

const getHeaders = () => {
    const token = localStorage.getItem("token");
    return {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    };
};

export const saveJob = async (job: any) => {
    return axios.post(`${BASE_URL}/tracking/save`, { job_id: job.job_id, job_data: job }, getHeaders());
};

export const markApplied = async (job: any) => {
    return axios.post(`${BASE_URL}/tracking/applied`, { job_id: job.job_id, job_data: job }, getHeaders());
};

export const markNotInterested = async (job: any) => {
    return axios.post(`${BASE_URL}/tracking/not-interested`, { job_id: job.job_id, job_data: job }, getHeaders());
};

// Updated to support pagination and filtering
export const getTrackedJobs = async (status: string = "saved", page: number = 1, limit: number = 9) => {
    return axios.get(`${BASE_URL}/tracking/list`, {
        ...getHeaders(),
        params: { status, page, limit }
    });
};

export const getJobStatus = async (jobId: string) => {
    return axios.get(`${BASE_URL}/tracking/status/${jobId}`, getHeaders());
};
