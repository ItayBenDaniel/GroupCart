import axios from "axios"
import * as SecureStore from "expo-secure-store"

const api = axios.create({ baseURL: "http://10.100.102.23:8002" });

api.interceptors.request.use(async (config) => {
    const token = await SecureStore.getItemAsync("access_token")
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export default api;