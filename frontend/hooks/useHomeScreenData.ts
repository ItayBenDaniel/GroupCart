import { useEffect, useState } from "react";
import axios from "axios";

export type StoreProduct = {
    id: number;
    name: string;
    price: number;
    quantity: string;
    item_code: string;
    original_price?: number;
    unit_of_measure: string;
};

export default function useHomeScreenData() {
    const [username, setUsername] = useState("");
    const [randomProducts, setRandomProducts] = useState<StoreProduct[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        let isMounted = true;
        setLoading(true);

        // Create promises for both API calls
        const userPromise = axios.get("http://10.100.102.9:8002/users/users/1")
            .then((res) => {
                if (isMounted) setUsername(res.data.username);
            })
            .catch((err) => {
                if (isMounted) console.error("Failed to fetch user", err);
            });

        const productsPromise = axios.get("http://10.100.102.9:8002/store_products/random/10")
            .then((res) => {
                if (isMounted) setRandomProducts(res.data);
            })
            .catch((err) => {
                if (isMounted) console.error("Failed to fetch products", err);
            });

        // Wait for both promises to resolve
        Promise.all([userPromise, productsPromise])
            .finally(() => {
                if (isMounted) setLoading(false);
            });

        return () => { isMounted = false };
    }, []);

    return { username, randomProducts, loading };
}