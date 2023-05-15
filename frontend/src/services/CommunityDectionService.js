import axios from 'axios';
const API_BASE_URL = 'http://127.0.0.1:8000/search/';
const COMMUNITIES_URL = 'get_keyword_author_commonities/';

const getCommunityData = async () => {
    try {
        const response = await axios.get(API_BASE_URL + COMMUNITIES_URL);
        return response.data;
    } catch (error) {
        console.error(error);
        throw new Error('Failed to fetch data');
    }
};

export { getCommunityData }