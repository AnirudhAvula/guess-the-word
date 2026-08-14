import axios from "axios";

const API = axios.create({
    baseURL: "https://guess-the-word-mmqb.onrender.com",
});

export default API;