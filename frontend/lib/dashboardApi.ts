import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const getDashboardSummary = async (token: string) => {
    try {
        const response = await axios.get(`${API_URL}/dashboard/summary`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        return response.data;
    } catch (error) {
        console.error('Error fetching dashboard summary:', error);
        throw error;
    }
};

export const getSkillAnalytics = async (token: string) => {
    try {
        const response = await axios.get(`${API_URL}/dashboard/skills`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        return response.data;
    } catch (error) {
        console.error('Error fetching skill analytics:', error);
        throw error;
    }
};
