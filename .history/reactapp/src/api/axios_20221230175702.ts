import axios from "axios"
export const BASE_PATH = process.env.REACT_APP_API

export const api = axios.create({
    baseURL: BASE_PATH,
});

export const axiosPrivate = axios.create({
    baseURL: BASE_PATH,
    //withCredentials: true
});