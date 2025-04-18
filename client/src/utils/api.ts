import axios from "axios";

const api = axios.create({
    baseURL: 'http://localhost:8000/api/v1/', // Hardcode localhost for browser access
    timeout: 5000,
});

export default api;
