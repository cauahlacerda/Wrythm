import axios from "axios";
import 'dotenv/config';

const baseURL = process.env.AI_RESUMER_BASE_URL as string

const AIResumerAPI = axios.create({
    baseURL: baseURL || "http://localhost:8000",
    timeout: 10000,
});

export default AIResumerAPI;