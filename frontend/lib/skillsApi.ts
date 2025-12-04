import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const getSkillAnalysis = async (token: string) => {
    try {
        const response = await axios.get(`${API_URL}/skills/analysis`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        return response.data;
    } catch (error) {
        console.error('Error fetching skill analysis:', error);
        throw error;
    }
};
