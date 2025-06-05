import * as SecureStore from "expo-secure-store";
import { jwtDecode } from "jwt-decode";

type TokenPayload = {
    sub: string;
    exp: number; // in seconds since epoch
};

export async function checkTokenExpired() {
    const token = await SecureStore.getItemAsync("access_token");
    if (!token) return;

    try {
        const decoded = jwtDecode<TokenPayload>(token);
        const nowInSeconds = Math.floor(Date.now() / 1000);
        console.log("Checking token")

        if (decoded.exp < nowInSeconds == true) {
            await SecureStore.deleteItemAsync("access_token");
            console.log("Deleted token")
        }
    } catch (err) {
        console.error("Failed to decode token:", err);
    }
}