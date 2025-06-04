import axios from "axios"
import * as SecureStore from "expo-secure-store"

const api = axios.create({ baseURL: "http://192.168.68.52:8002" });

api.interceptors.request.use(async (config) => {
    const token = await SecureStore.getItemAsync("access_token")
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export default api;