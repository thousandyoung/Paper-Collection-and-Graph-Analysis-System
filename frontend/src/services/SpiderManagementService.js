import axios from 'axios';
const API_BASE_URL = 'http://127.0.0.1:8000/spider/';
const SPIDERS_URL = 'spiders/'

export const fetchSpiders = async () => {
    try {
        const res = await axios.get(API_BASE_URL+SPIDERS_URL);
        return res.data;
    } catch (error) {
        throw new Error('Failed to fetch spiders');
    }
};

export const addSpider = async (values) => {
    try {
        await axios.post(API_BASE_URL+SPIDERS_URL, values);
        return 'Spider added successfully';
    } catch (error) {
        throw new Error('Failed to add spider');
    }
};

export const deleteSpider = async (spider) => {
    try {
        await axios.delete(API_BASE_URL+SPIDERS_URL+`${spider.id}/`);
        return 'Spider deleted successfully';
    } catch (error) {
        throw new Error('Failed to delete spider');
    }
};

