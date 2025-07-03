import { View, Text, Image, ScrollView, TouchableOpacity, Alert } from "react-native";
import { Ionicons } from "@expo/vector-icons";
import { useEffect, useState } from "react";
import * as Location from "expo-location";
import BuyButton from "./buttons/BuyButton";
import api from "../lib/axios";

type Props = {
    product_id: number;
    item_code: string;
    image: any;
    name: string;
    quantity: string;
    price: string;
    unit_of_measure: string;
    oldPrice?: string;
    sale?: number;
    isFavorite?: boolean;
    onClose?: () => void;
};

export default function ProductDetails({
    product_id,
    item_code,
    image,
    name,
    quantity,
    price,
    unit_of_measure,
    oldPrice,
    sale,
    onClose,
}: Props) {
    const [storeOptions, setStoreOptions] = useState<any[]>([]);
    const [loadingStores, setLoadingStores] = useState(false);
    const [liked, setLiked] = useState(false);
    const finalPrice = price;
    const old_price = oldPrice ?? price;
    if (!sale) {
        sale = 1
    }
    const toggleLike = async () => {
        try {
            if (!liked) {
                await api.post(`/likes/${product_id}`);
            }
            else {
                await api.delete(`/likes/${product_id}`);
            }
            setLiked(!liked);
        } catch (err) {
            console.error("Failed to toggle like:", err);
        }
    };

    const handleAddToCart = async () => {
        try {
            const res = await api.post("/cart/", {
                store_product_id: product_id,
                quantity: 1,
            });

            Alert.alert("המוצר נוסף לסל 🎉");
        } catch (err) {
            console.error("Failed to add to cart:", err);
            Alert.alert("שגיאה", "לא ניתן להוסיף את המוצר לסל");
        }
    };

    useEffect(() => {
        const fetchStores = async () => {
            if (!item_code) return;
            try {
                setLoadingStores(true);

                const { status } = await Location.requestForegroundPermissionsAsync();
                if (status !== "granted") return;

                let loc = await Location.getLastKnownPositionAsync();
                if (!loc) loc = await Location.getCurrentPositionAsync({});

                const { latitude, longitude } = loc.coords;

                const res = await api.get(
                    `/store_products/nearby_stores_with_product?item_code=${item_code}&lat=${latitude}&lon=${longitude}`
                );
                setStoreOptions(res.data);
            } catch (err) {
                console.error("Failed to fetch store options:", err);
            } finally {
                setLoadingStores(false);
            }
        };

        fetchStores();
    }, []);

    return (
        <View className="flex-1 bg-white">
            <TouchableOpacity onPress={onClose} className="absolute top-10 left-4 z-50">
                <Ionicons name="close" size={28} color="black" />
            </TouchableOpacity>

            <View className="bg-white pt-10 pb-2 items-center">
                <View className="w-56 h-56 rounded-full bg-white  items-center justify-center">
                    <Image source={image} className="w-48 h-48" resizeMode="contain" />
                </View>
            </View>

            <View className="px-5 pt-10 gap-y-3">
                <TouchableOpacity onPress={toggleLike} className="ml-3 items-end">
                    <Ionicons
                        name={liked ? "heart" : "heart-outline"}
                        size={36}
                        color={liked ? "red" : "gray"}
                    />
                </TouchableOpacity>
                <View className="flex-row justify-between items-center">
                    <Text className="text-3xl font-interBold text-right flex-1">{name}</Text>

                </View>

                <View className="flex-row rtl:space-x-reverse gap-x-2">
                    <Text className="text-2xl font-interBold">₪ {price}</Text>
                    {oldPrice && (
                        <Text className="text-m line-through text-gray-400">₪ {oldPrice}</Text>
                    )}
                </View>

                <Text className="text-right text-sm text-gray-600">
                    {quantity} {unit_of_measure}
                </Text>
            </View>

            {/* Store slider */}
            <View className="mt-4 px-4">
                <Text className="text-right text-base font-bold mb-2">חנויות קרובות</Text>
                {loadingStores ? (
                    <Text className="text-center text-gray-500">טוען חנויות...</Text>
                ) : storeOptions.length === 0 ? (
                    <Text className="text-center text-gray-400">לא נמצאו חנויות קרובות</Text>
                ) : (
                    <ScrollView horizontal showsHorizontalScrollIndicator={false}>
                        {storeOptions.map((store, i) => (
                            <View
                                key={i}
                                className="bg-white px-5 py-3 mr-4 rounded-xl shadow-sm border border-gray-200 w-40"
                            >
                                <Text className="text-right text-sm font-bold text-gray-800">{store.store_name}</Text>
                                <Text className="text-right text-xs text-gray-500 mt-1">{store.distance_km} ק"מ</Text>
                                <Text className="text-right text-sm text-orange-600 font-bold mt-2">
                                    ₪ {store.price.toFixed(2)}
                                </Text>
                                <Image
                                    source={{ uri: `http://10.100.102.23:8002/static/icons/${store.chain_id}.png` }}
                                    className="w-20 h-20 self-center mt-3"
                                    resizeMode="contain"
                                />
                            </View>
                        ))}
                    </ScrollView>
                )}
            </View>

            {/* Add to cart button */}
            <BuyButton button_text="הוסף לסל" handleAddToCart={handleAddToCart} />
        </View>
    );
}
