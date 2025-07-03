// hooks/useCartData.ts
import { useEffect, useState } from "react";
import axios from "axios";
import api from "../lib/axios";

export type CartItem = {
    id: number;
    name: string;
    price: number;
    item_code: string;
    quantity: string;
    unit_of_measure: string;
    added_by: string;
};

export default function useCartData() {
    const [cartItems, setCartItems] = useState<CartItem[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchCart = async () => {
            try {
                const res = await api.get("/cart/full");
                setCartItems(res.data);
            } catch (err) {
                //console.error("Failed to load cart", err);
            } finally {
                setLoading(false);
            }
        };

        fetchCart();
    }, []);

    return { cartItems, setCartItems, loading };
}
