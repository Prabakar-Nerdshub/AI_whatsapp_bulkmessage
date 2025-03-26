import axios from "axios";

const apiClient = axios.create({
    baseURL: process.env.REACT_APP_BASE_API_URL || "http://127.0.0.1:8000",
    headers: {
        "Content-Type": "application/json",
    },
});

export default apiClient;
