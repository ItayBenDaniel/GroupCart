import * as SecureStore from "expo-secure-store";
import { jwtDecode } from "jwt-decode";

type TokenPayload = {
    sub: string;
    exp: number;
};

export async function getUserIdFromToken(): Promise<number | null> {
    const token = await SecureStore.getItemAsync("access_token");
    if (!token) return null;

    try {
        const decoded = jwtDecode<TokenPayload>(token);
        return parseInt(decoded.sub);
    } catch (err) {
        console.error("Failed to decode token:", err);
        return null;
    }
}
