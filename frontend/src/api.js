import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

export const scrapeUserData = (username) => {
    return axios.post('${API_BASE_URL}/scrape', { username });
};

export const compareUsers = (usernames) => {
    return axios.post('${API_BASE_URL}/compare', { usernames });
};

export const displayComparison = (plotId) => {
    return axios.post('${API_BASE_URL}/display_comparison', { params: { "plot_id": plotId } });
};

export const showScrapedData = (username) => {
    return axios.post('${API_BASE_URL}/craped_user', { username });
};

export const checkUserExists = (username) => {
    return axios.post('${API_BASE_URL}/existing', { username });
};

export const clearMongoCollection = (username) => {
    return axios.post('${API_BASE_URL}/clear', { username });
};

export const checkRepoSimilarity = (usernames) => {
    return axios.post('${API_BASE_URL}/similarity', { usernames });
};

export const compileGraph = (usernames) => {
    return axios.post('${API_BASE_URL}/graph', { usernames });
};

export const displayGraph = (graphId) => {
    return axios.post('${API_BASE_URL}/display_graph', { params: { "graph_id": graph_id } });
};
