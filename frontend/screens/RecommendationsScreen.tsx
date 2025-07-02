import { View, Text, ScrollView, TouchableOpacity, Image } from "react-native";
import { useEffect, useState } from "react";
import { useRouter } from "expo-router";
import { Ionicons } from "@expo/vector-icons";
import api from "../lib/axios";
import { Alert } from "react-native";

export default function RecommendationsScreen() {
    const [recommendations, setRecommendations] = useState<any[]>([]);
    const [selected, setSelected] = useState<number[]>([]);
    const [selectedTab, setSelectedTab] = useState<string>("מומלצים");
    const tabs = ["קניתי בעבר", "הנחות", "מומלצים"];

    const router = useRouter();

    useEffect(() => {
        const fetchRecommendations = async () => {
            try {
                const res = await api.get("/recommendations/family");
                setRecommendations(res.data);
            } catch (error) {
                console.error("Failed to load recommendations:", error);
            }
        };

        fetchRecommendations();
    }, []);

    const toggleSelect = (id: number) => {
        setSelected((prev) =>
            prev.includes(id) ? prev.filter((i) => i !== id) : [...prev, id]
        );
    };
    const handleAddToCart = async () => {
        try {
            await api.post("/cart/bulk/",
                { items: selected.map((id) => ({ store_product_id: id, quantity: 1 })), }
            )
            Alert.alert("המוצרים נוספו בהצלחה!")
            router.push("/cart")
        }
        catch (err) {
            console.error("Failed to bulk add to cart", err);
        }
    }
    return (
        <View className="flex-1 bg-white pt-16">
            <View className="px-6 mb-4">
                <View className="flex-row justify-between items-center mb-2">
                    <Text className="text-xl font-bold text-right flex-1">מוצרים מומלצים</Text>
                    <TouchableOpacity onPress={() => router.back()} className="border border-gray-400 p-2 rounded-xl bg-gray-50 ml-4">
                        <Ionicons name="arrow-forward-circle-outline" size={24} color="#F17547" />
                    </TouchableOpacity>
                </View>
                {/* Tabs */}
                <View className="flex-row justify-end mt-4 mb-4 space-x-2 space-x-reverse">
                    {tabs.map((tab) => (
                        <TouchableOpacity
                            key={tab}
                            onPress={() => setSelectedTab(tab)}
                            className={`mx-1 px-4 py-2 rounded-full ${selectedTab === tab ? "bg-orange-500" : "bg-gray-100"
                                }`}
                        >
                            <Text className={`font-bold ${selectedTab === tab ? "text-white" : "text-gray-700"}`}>
                                {tab}
                            </Text>
                        </TouchableOpacity>
                    ))}
                </View>
            </View>

            <ScrollView className="px-6 mb-20">
                {recommendations.map((product, index) => (
                    <TouchableOpacity
                        key={index}
                        className={`flex-row justify-between items-center mb-4  rounded-2xl p-4 ${selected.includes(product.id)
                            ? "bg-orange-50 border border-orange-300"
                            : "bg-gray-100"
                            }`}
                        onPress={() => toggleSelect(product.id)}
                    >
                        {/* Image (left) */}
                        {product.has_image ? (
                            <Image
                                source={{ uri: `http://10.100.102.23:8002/static/icons/${product.item_code}.png` }}
                                className="w-16 h-16 rounded-md"
                                resizeMode="contain"
                            />
                        ) : (
                            <View className="w-16 h-16 bg-gray-300 rounded-md" />
                        )}


                        {/* Product details (middle) */}
                        <View className="flex-1 mr-4">
                            <Text className="text-right font-bold text-gray-800 mb-1">{product.name}</Text>
                            <Text className="text-right text-sm text-gray-500">
                                ₪ {product.price?.toFixed(2) ?? "?"}
                            </Text>
                        </View>
                        {/* Checkbox (right) */}
                        <View className="w-6 h-6 border-2 border-gray-400 rounded-sm">
                            {selected.includes(product.id) && (
                                <View className="bg-orange-500 w-full h-full rounded-sm" />
                            )}
                        </View>

                    </TouchableOpacity>
                ))}
                <View className="h-6" />
                <TouchableOpacity className="bg-orange-500 py-4 rounded-full mb-20" onPress={handleAddToCart}>
                    <Text className="text-center text-white text-lg font-bold">
                        הוסף והמשך לתשלום
                    </Text>
                </TouchableOpacity>
            </ScrollView>


        </View>
    );
}
