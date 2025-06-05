import { useEffect, useState, useCallback } from "react";
import * as SecureStore from "expo-secure-store";
import { jwtDecode } from "jwt-decode";
import { useFocusEffect } from "expo-router"; // or @react-navigation/native if using that

type TokenPayload = {
    sub: string;
    exp: number;
};

export function useAuth() {
    const [loggedIn, setLoggedIn] = useState(false);

    async function checkToken() {
        const token = await SecureStore.getItemAsync("access_token");
        if (!token) return setLoggedIn(false);

        try {
            const decoded = jwtDecode<TokenPayload>(token);
            const now = Math.floor(Date.now() / 1000);
            setLoggedIn(decoded.exp > now);
        } catch {
            setLoggedIn(false);
        }
    }

    useFocusEffect(
        useCallback(() => {
            checkToken();
        }, [])
    );

    return loggedIn;
}
