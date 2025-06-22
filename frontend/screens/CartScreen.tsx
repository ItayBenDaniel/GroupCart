import { View, Text, TouchableOpacity, FlatList, ActivityIndicator, Image, Alert } from "react-native";
import useCartData from "../hooks/useCartData";
import BottomNav from "../components/BottomNav";
import BuyButton from "../components/buttons/BuyButton"
import { useState } from "react";
import { CartItem } from "../hooks/useCartData";
import { Ionicons } from "@expo/vector-icons";
import { useEffect } from "react";
import { useRouter } from "expo-router";
import dayjs from "dayjs";
import axios from "axios";
import api from "../lib/axios";

export default function CartScreen() {
    type ActionHistoryItem = {
        username: string;
        name: string,
        action: string;
        quantity: number;
        timestamp: string;
    };
    const { cartItems, setCartItems, loading } = useCartData();
    const [editingItemId, setEditingItemId] = useState<number | null>(null);
    const [showHistory, setShowHistory] = useState(false);
    const [actionHistory, setActionHistory] = useState<ActionHistoryItem[]>([]);
    const router = useRouter();
    const fetchHistory = async () => {
        try {
            console.log("HERE!123")
            const res = await api.get("/history/");
            console.log("HERE!1234 ")
            setActionHistory(res.data);
        } catch (err) {
            console.error("Failed to fetch history:", err);
        }
    };
    useEffect(() => {
        fetchHistory();
    }, []);


    if (loading) {
        return (
            <View className="flex-1 justify-center items-center bg-white">
                <ActivityIndicator size="large" color="#f97316" />
            </View>
        );
    }

    if (cartItems.length === 0) {
        return (
            <View className="flex-1 justify-center items-center bg-white">
                <Text className="text-gray-500 text-base">העגלה ריקה</Text>
            </View>
        );
    }
    const handleBuyCart = async () => {
        const cartPayload = {
            items: cartItems.map(item => ({
                product_id: item.id, // or item.store_product.id if nested
                quantity: item.quantity,
            }))
        };
        console.log("CART IS ", cartPayload)

        try {
            const res = await api.post("/purchases/", cartPayload,);

            Alert.alert("הקנייה התבצעה בהצלחה🎉");
            setCartItems([]);
            router.push("/recommendations")
        } catch (err) {
            console.error("Failed to add to cart:", err);
            Alert.alert("שגיאה", "לא ניתן להוסיף את המוצר לסל");
        }
    };



    const undoLastChange = async () => {
        try {
            await api.post("/history/undo");
            await fetchHistory();
            const updatedCart = await api.get("/cart/full");
            setCartItems(updatedCart.data);
        } catch (err) {
            console.error("Undo failed:", err);
        }
    };

    const redoLastUndo = async () => {
        try {
            await api.post("/history/redo");
            await fetchHistory();
            const updatedCart = await api.get("/cart/full");
            setCartItems(updatedCart.data);
        } catch (err) {
            console.error("Redo failed:", err);
        }
    };

    const totalPrice = cartItems.reduce(
        (sum, item) => sum + item.price * parseInt(item.quantity),
        0
    );

    const markAsPurchased = async (id: number) => {
        try {
            await api.patch(`/cart/${id}/mark_purchased`);
            const updated = await api.get("/cart/full");
            setCartItems(updated.data);
            fetchHistory(); // Optional if you want to log this too
        } catch (err) {
            console.error("Failed to mark as purchased", err);
        }
    };


    const updateQuantity = async (id: number, change: number) => {
        const item = cartItems.find(i => i.id === id);
        if (!item) return;

        try {
            const newQty = Math.max(1, parseInt(item.quantity) + change);
            console.log("WOWWOWOWOW")
            await api.patch(`/cart/${id}`, { quantity: newQty });
            const updated = cartItems.map(i => i.id === id ? { ...i, quantity: newQty.toString() } : i);
            setCartItems(updated);
            fetchHistory();
        } catch (err) {
            console.error("Failed to update quantity", err);
        }
    };

    const deleteItem = async (id: number) => {
        try {
            await api.delete(`/cart/${id}`);
            const updated = cartItems.filter(i => i.id !== id);
            setCartItems(updated);
            fetchHistory();
        } catch (err) {
            console.error("Failed to delete item", err);
        }
    };
    return (
        <View className="flex-1 relative bg-white">

            <Text className=" text-right text-3xl font-bold mr-5 mt-10 mb-10">עגלת קניות</Text>

            <View className="items-end mb-4 px-5">
                <TouchableOpacity
                    onPress={() => router.push("/recommendations")}
                    className="bg-orange-100 border border-orange-300 flex-row-reverse items-center px-4 py-3 rounded-2xl"
                >
                    <Text className="text-orange-800 font-semibold text-base ml-2">מוצרים מומלצים</Text>
                    <Ionicons name="sparkles-outline" size={20} color="#F17547" />
                </TouchableOpacity>
            </View>
            <TouchableOpacity
                onPress={() => setShowHistory(!showHistory)}
                className="self-end mr-5 mb-3"
            >
                <Text className="text-blue-500 text-sm">
                    {showHistory ? "הסתר היסטוריה" : "הצג היסטוריית שינויים"}
                </Text>
            </TouchableOpacity>

            {showHistory && (
                actionHistory.length === 0 ? (
                    <Text className="text-right text-sm text-gray-500">אין שינויים</Text>
                ) : (
                    actionHistory.map((action, index) => (
                        <Text key={index} className="text-right text-sm text-gray-700 mb-1 mr-2">
                            {action.username || "מישהו"} {action.action === "add" ? "הוסיף" :
                                action.action === "delete" ? "מחק" :
                                    action.action === "update" ? "עדכן" : action.action} את {action.name} ({action.quantity}) בתאריך {dayjs(action.timestamp).format("DD/MM/YYYY HH:mm")}
                        </Text>
                    ))
                )
            )}
            <View className="flex-row justify-end space-x-4 rtl:space-x-reverse px-5 mb-4">

                <TouchableOpacity onPress={undoLastChange} className="ml-3 border border-gray-400 p-2 rounded-xl bg-gray-50">
                    <Ionicons name="arrow-undo" size={28} color="#F17547" />
                </TouchableOpacity>


                <TouchableOpacity onPress={redoLastUndo} className="ml-3 border border-gray-400 p-2 rounded-xl bg-gray-50">
                    <Ionicons name="arrow-redo" size={28} color="#F17547" />
                </TouchableOpacity>

            </View>
            <FlatList
                data={cartItems}
                keyExtractor={(item) => item.id.toString()}
                contentContainerStyle={{
                    padding: 20,
                    paddingBottom: 0,
                }}
                renderItem={({ item }) => {

                    return (
                        <View className="bg-gray-50 border border-gray-200 p-4 rounded-xl mb-4">
                            <View className="flex-row items-center">
                                <Image
                                    source={{
                                        uri: `http://10.100.102.23:8002/static/icons/${item.item_code}.png`,
                                    }}
                                    className="w-16 h-16 ml-4"
                                    resizeMode="contain"
                                />

                                <View className="flex-1">
                                    <Text className="text-right font-interSemi text-sm">{item.name}</Text>
                                    <Text className="text-right text-s text-gray-500 mt-1">
                                        {(parseInt(item.quantity) * item.price).toFixed(2)}₪
                                    </Text>
                                    {item.added_by && (
                                        <Text className="text-right text-[11px] text-gray-400 mt-0.5">
                                            נוסף על ידי: {item.added_by}
                                        </Text>
                                    )}

                                    <TouchableOpacity
                                        onPress={() =>
                                            setEditingItemId(editingItemId === item.id ? null : item.id)
                                        }
                                    >
                                        <Text className="text-xs text-app_orange text-right mt-1">ערוך</Text>
                                    </TouchableOpacity>
                                </View>
                            </View>

                            {editingItemId === item.id && (
                                <View className="flex-row justify-end items-center mt-4 space-x-4 rtl:space-x-reverse">
                                    <TouchableOpacity
                                        onPress={() => updateQuantity(item.id, -1)}
                                        className="bg-white border border-gray-300 w-8 h-8 rounded-full items-center justify-center mx-1"
                                    >
                                        <Text className="text-lg text-orange-500">−</Text>
                                    </TouchableOpacity>

                                    <Text className="text-lg font-bold w-6 text-center">{item.quantity}</Text>

                                    <TouchableOpacity
                                        onPress={() => updateQuantity(item.id, 1)}
                                        className="bg-white border border-gray-300 w-8 h-8 rounded-full items-center justify-center mx-1"
                                    >
                                        <Text className="text-lg text-orange-500">+</Text>
                                    </TouchableOpacity>

                                    <TouchableOpacity onPress={() => deleteItem(item.id)}>
                                        <Text className="text-s text-red-500 ml-5">🗑️</Text>
                                    </TouchableOpacity>
                                    <TouchableOpacity
                                        onPress={() => markAsPurchased(item.id)}
                                        className="ml-2 bg-green-500 px-2 py-1 rounded"
                                    >
                                        <Text className="text-white text-xs">נרכש</Text>
                                    </TouchableOpacity>
                                </View>
                            )}
                        </View>
                    );
                }}
                ListFooterComponent={
                    <View>
                        <Text className="text-right text-lg font-bold mb-3 mr-5">
                            סך הכול: ₪{totalPrice.toFixed(2)}
                        </Text>
                        <BuyButton button_text="קנה עכשיו" handleAddToCart={handleBuyCart} />
                    </View>
                }

            />
            <BuyButton button_text="קנה" handleAddToCart={handleBuyCart}></BuyButton>
        </View>

    );
}
