import { useEffect, useState } from "react";
import api from "../lib/axios";

export type StoreProduct = {
    id: number;
    name: string;
    price: number;
    quantity: string;
    item_code: string;
    unit_of_measure: string;
    category: string;
    promotion_price?: number | null;

};

export default function useHomeScreenData() {
    const [randomProducts, setRandomProducts] = useState<StoreProduct[]>([]);
    const [loading, setLoading] = useState(true);

    const [likedIds, setLikedIds] = useState<Set<number>>(new Set());

    useEffect(() => {
        let isMounted = true;
        setLoading(true);

        const productsPromise = api.get("/store_products/random/100")
            .then((res) => {
                if (isMounted) {
                    setRandomProducts(res.data);
                }

            })
            .catch((err) => {
            });

        const likesPromise = api.get("/likes/")
            .then((res) => {
                if (isMounted) setLikedIds(new Set(res.data.map((item: any) => item.id)));
            })
            .catch((err) => {
            });

        Promise.all([productsPromise, likesPromise])
            .finally(() => {
                if (isMounted) setLoading(false);
            });

        return () => { isMounted = false };
    }, []);

    const toggleLike = async (productId: number) => {
        const isLiked = likedIds.has(productId);
        try {
            if (isLiked) {
                await api.delete(`/likes/${productId}`);
                setLikedIds((prev) => {
                    const updated = new Set(prev);
                    updated.delete(productId);
                    return updated;
                });
            } else {
                await api.post(`/likes/${productId}`);
                setLikedIds((prev) => new Set(prev).add(productId));
            }
        } catch (err) {
            console.error("Failed to toggle like:", err);
        }
    };

    return {
        randomProducts,
        loading,
        likedIds,
        toggleLike,
    };
}
