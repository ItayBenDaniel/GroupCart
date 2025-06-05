// hooks/useCartData.ts
import { useEffect, useState } from "react";
import axios from "axios";
import api from "../lib/axios";
import { getUserIdFromToken } from "../lib/getUserIdFromToken";

export type User = {
    id: number;
    username: string;
    email: string;
};

export default function useUserData() {
    const [user, setUser] = useState<User | null>(null);

    useEffect(() => {
        (async () => {
            const userId = await getUserIdFromToken();
            try {
                const res = await api.get(`/users/users/${userId}`);
                setUser(res.data);
            } catch (err) {
                console.error("Failed to fetch user data:", err);
                setUser(null);
            }
        })();
    }, []);

    return { user };
}
