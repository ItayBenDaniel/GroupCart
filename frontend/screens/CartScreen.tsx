import { View, Text, TouchableOpacity, FlatList, ActivityIndicator, Image, Alert } from "react-native";
import useCartData from "../hooks/useCartData";
import BottomNav from "../components/BottomNav";
import BuyButton from "../components/buttons/BuyButton"
import axios from "axios";
import api from "../lib/axios";
import { useState } from "react";
import { CartItem } from "../hooks/useCartData";
import { Ionicons } from "@expo/vector-icons";

export default function CartScreen() {
    const { cartItems, setCartItems, loading } = useCartData();
    const [editingItemId, setEditingItemId] = useState<number | null>(null);
    const [undoStack, setUndoStack] = useState<CartItem[][]>([]);
    const [redoStack, setRedoStack] = useState<CartItem[][]>([]);
    const [showHistory, setShowHistory] = useState(false);
    const [actionHistory, setActionHistory] = useState<CartAction[]>([]);


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
        } catch (err) {
            console.error("Failed to add to cart:", err);
            Alert.alert("שגיאה", "לא ניתן להוסיף את המוצר לסל");
        }
    };



    const totalPrice = cartItems.reduce(
        (sum, item) => sum + item.price * parseInt(item.quantity),
        0
    );

    const pushToUndoStack = () => {
        setUndoStack(prev => [...prev, cartItems]);
        setRedoStack([]); // clear redo stack on any new action
    };

    const undoLastChange = () => {
        if (undoStack.length === 0) return;

        const last = undoStack[undoStack.length - 1];
        setUndoStack(prev => prev.slice(0, -1));
        setRedoStack(prev => [...prev, cartItems]);
        setCartItems(last);

        // Remove last visible action from log
        setActionHistory(prev => prev.slice(0, -1));
    };

    const redoLastUndo = () => {
        if (redoStack.length === 0) return;

        const last = redoStack[redoStack.length - 1];
        setRedoStack(prev => prev.slice(0, -1));
        setUndoStack(prev => [...prev, cartItems]);
        setCartItems(last);

        setActionHistory(prev => prev.slice(0, -1));
    };

    const updateQuantity = (id: number, change: number) => {
        const item = cartItems.find(i => i.id === id);
        if (!item) return;
        pushToUndoStack(); // <-- this was missing

        const newQty = Math.max(1, parseInt(item.quantity) + change).toString();

        setActionHistory(prev => [
            ...prev,
            {
                type: change > 0 ? "add" : "remove",
                user: item.added_by || "מישהו",
                itemName: item.name,
                timestamp: Date.now()
            }
        ]);

        setCartItems(prev =>
            prev.map(i =>
                i.id === id ? { ...i, quantity: newQty } : i
            )
        );
    };

    const deleteItem = (id: number) => {
        const item = cartItems.find(i => i.id === id);
        if (!item) return;
        pushToUndoStack(); // <-- this was also missing

        setActionHistory(prev => [
            ...prev,
            {
                type: "delete",
                user: item.added_by || "מישהו",
                itemName: item.name,
                timestamp: Date.now()
            }
        ]);

        setCartItems(prev => prev.filter(i => i.id !== id));
    };
    return (
        <View className="flex-1 relative bg-white">

            <Text className=" text-right text-3xl font-bold mr-5 mt-10 mb-10">עגלת קניות</Text>

            <TouchableOpacity
                onPress={() => setShowHistory(!showHistory)}
                className="self-end mr-5 mb-3"
            >
                <Text className="text-blue-500 text-sm">
                    {showHistory ? "הסתר היסטוריה" : "הצג היסטוריית שינויים"}
                </Text>
            </TouchableOpacity>

            {showHistory && (
                <View className="bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 mx-5 mb-4">
                    {actionHistory.length === 0 ? (
                        <Text className="text-right text-sm text-gray-500">אין שינויים</Text>
                    ) : (
                        actionHistory.map((action, index) => (
                            <Text key={index} className="text-right text-sm text-gray-700 mb-1">
                                {action.user} {action.type === "add" ? "הוסיף" : action.type === "remove" ? "הסיר" : "מחק"} את {action.itemName}
                            </Text>
                        ))
                    )}
                </View>
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
                                        uri: `http://192.168.68.52:8002/static/icons/${item.item_code}.png`,
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
