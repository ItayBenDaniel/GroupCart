import { View, Text, TouchableOpacity } from "react-native";
import { useEffect, useState } from "react";
import { useRouter } from "expo-router";
import * as SecureStore from "expo-secure-store";
import api from "../lib/axios";
import useUserData from "../hooks/useUserData";
import dayjs from 'dayjs';

export default function ProfileScreen() {
    const user = useUserData();
    const router = useRouter();
    const [showPurchases, setShowPurchases] = useState(false);
    const [purchases, setPurchases] = useState<any[]>([]);

    useEffect(() => {
        // const fetchUser = async () => {
        //     const token = await SecureStore.getItemAsync("token");
        //     if (token) {
        //         api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
        //         const res = await api.get("/users/me");
        //         setUsername(res.data.username);
        //     }
        // };
        // fetchUser();
    }, []);
    const togglePurchases = async () => {
        if (!showPurchases) {
            try {
                const res = await api.get("/purchases/");
                setPurchases(res.data);
            } catch (err) {
                console.error("Failed to fetch purchases:", err);
            }
        }
        setShowPurchases(!showPurchases);
    };

    return (
        <View className="flex-1 bg-white px-6 pt-16">
            <Text className="text-2xl font-bold text-right mb-6">שלום, {user?.user?.username}</Text>

            <TouchableOpacity
                onPress={togglePurchases}
                className="bg-gray-100 rounded-xl px-4 py-5 mb-4 shadow-sm"
            >
                <Text className="text-right text-lg font-semibold">
                    {showPurchases ? "הסתר רכישות" : "הצג רכישות קודמות"}
                </Text>
            </TouchableOpacity>
            {showPurchases && (
                <View className="bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 mb-4">
                    {purchases.length === 0 ? (
                        <Text className="text-right text-sm text-gray-500">אין רכישות קודמות</Text>
                    ) : (
                        purchases.map((purchase, index) => (
                            <View key={index} className="mb-3">
                                <Text className="text-right text-sm font-bold text-orange-600 mb-1">
                                    רכישה #{purchase.id}
                                </Text>
                                <Text className="text-right text-sm font-bold text-orange-600 mb-1">
                                    הרכישה התבצעה ב #{dayjs(purchase.purchased_at).format("DD/MM/YYYY HH:mm")}
                                </Text>
                                {purchase.items.map((item: any, i: number) => (
                                    <Text key={i} className="text-right text-xs text-gray-700">
                                        {item.product.name} — {item.quantity} יח'
                                    </Text>
                                ))}
                            </View>
                        ))
                    )}
                </View>
            )}

            <TouchableOpacity
                //onPress={() => router.push("/family")}
                className="bg-gray-100 rounded-xl px-4 py-5 mb-4 shadow-sm"
            >
                <Text className="text-right text-lg font-semibold">חברי המשפחה</Text>
            </TouchableOpacity>

            <TouchableOpacity
                onPress={async () => {
                    await SecureStore.deleteItemAsync("access_token");
                    router.replace("/signup");
                }}
                className="bg-orange-500 rounded-full py-4 mt-10"
            >
                <Text className="text-white font-bold text-center text-lg">התנתק</Text>
            </TouchableOpacity>
        </View>
    );
}
