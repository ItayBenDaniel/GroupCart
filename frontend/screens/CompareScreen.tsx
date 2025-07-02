import { useEffect, useState } from "react";
import {
    View,
    Text,
    ScrollView,
    TouchableOpacity,
    ActivityIndicator,
    Image
} from "react-native";
import { useRouter } from "expo-router";
import * as Location from "expo-location";
import api from "../lib/axios";

export default function ComparePricesScreen() {
    const [storePrices, setStorePrices] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const router = useRouter();
    const [sortBy, setSortBy] = useState<"price" | "distance">("price");

    useEffect(() => {
        (async () => {
            try {
                const { status } = await Location.requestForegroundPermissionsAsync();
                if (status !== "granted") {
                    setError("יש לאשר גישה למיקום");
                    setLoading(false);
                    return;
                }

                let loc = await Location.getLastKnownPositionAsync();
                if (!loc) loc = await Location.getCurrentPositionAsync({});

                const lat = loc.coords.latitude;
                const lon = loc.coords.longitude;

                const res = await api.get(`/cart/prices/compare?lat=${lat}&lon=${lon}`);
                setStorePrices(res.data);
            } catch (err) {
                console.error(err);
                setError("שגיאה באחזור נתוני סל הקניות.");
            } finally {
                setLoading(false);
            }
        })();
    }, []);

    if (loading) {
        return (
            <View className="flex-1 justify-center items-center bg-white">
                <ActivityIndicator size="large" color="#f97316" />
            </View>
        );
    }

    if (error) {
        return (
            <View className="flex-1 justify-center items-center bg-white">
                <Text className="text-red-500 text-center text-lg">{error}</Text>
            </View>
        );
    }

    return (
        <View className="flex-1 bg-white pt-16 px-6">
            <Text className="text-right text-2xl font-bold mb-6">השוואת סל קניות</Text>
            <View className="flex-row justify-end mb-4">
                <TouchableOpacity
                    onPress={() => setSortBy((prev) => (prev === "price" ? "distance" : "price"))}
                    className="bg-orange-200 px-4 py-2 rounded-lg"
                >
                    <Text className="text-sm font-medium text-orange-800">
                        מיין לפי {sortBy === "price" ? "מרחק" : "מחיר"}
                    </Text>
                </TouchableOpacity>
            </View>
            <ScrollView className="mb-20">
                {storePrices.length === 0 ? (
                    <Text className="text-center text-gray-500 mt-10">
                        לא נמצאו חנויות בקרבתך שמחזיקות את כל המוצרים.
                    </Text>
                ) : (
                    storePrices
                        .slice()
                        .sort((a, b) =>
                            sortBy === "price"
                                ? a.total_price - b.total_price
                                : a.distance_km - b.distance_km
                        )
                        .map((store, index) => (
                            <View
                                key={index}
                                className="flex-row items-center bg-gray-100 rounded-xl p-4 mb-4 border border-orange-200"
                            >
                                {/* Logo */}
                                <Image
                                    source={{
                                        uri: `http://10.100.102.23:8002/static/icons/${store.chain_id}.png`,
                                    }}
                                    className="w-24 h-24 mr-4"
                                    resizeMode="contain"
                                />

                                {/* Info */}
                                <View className="flex-1">
                                    <Text className="text-right font-bold text-lg mb-1">{store.store_name}</Text>
                                    <Text className="text-right text-sm text-gray-600">{store.address}</Text>
                                    <Text className="text-right text-sm text-gray-500 mt-1">
                                        מרחק: {store.distance_km} ק"מ
                                    </Text>
                                    <Text className="text-right text-lg text-orange-600 font-bold mt-2">
                                        מחיר סל: ₪{store.total_price.toFixed(2)}
                                    </Text>
                                </View>
                            </View>
                        ))
                )}
            </ScrollView>

            <TouchableOpacity
                onPress={() => router.back()}
                className="bg-orange-500 rounded-full py-4 mt-6"
            >
                <Text className="text-center text-white text-lg font-bold">חזור</Text>
            </TouchableOpacity>
        </View>
    );
}
