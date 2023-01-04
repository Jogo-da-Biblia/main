import axios from "axios"
export const BASE_URL = process.env.REACT_APP_API

export const api = axios.create({
    baseURL: BASE_URL,
});

export const axiosPrivate = axios.create({
    baseURL: BASE_URL,
    //withCredentials: true
});