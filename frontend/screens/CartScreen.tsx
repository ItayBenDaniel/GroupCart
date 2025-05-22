import { View, Text, FlatList, ActivityIndicator, Image, Alert } from "react-native";
import useCartData from "../hooks/useCartData";
import BottomNav from "../components/BottomNav";
import BuyButton from "../components/buttons/BuyButton"
import axios from "axios";

export default function CartScreen() {
    const { cartItems, loading } = useCartData();

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
            const res = await axios.post("http://10.100.102.9:8002/purchases/", cartPayload,);

            Alert.alert("הקנייה התבצעה בהצלחה🎉");
        } catch (err) {
            console.error("Failed to add to cart:", err);
            Alert.alert("שגיאה", "לא ניתן להוסיף את המוצר לסל");
        }
    };
    return (
        <View className="flex-1 relative">
            <Text className=" text-right text-3xl font-bold mr-5 mt-10 mb-10">עגלת קניות</Text>

            <FlatList
                data={cartItems}
                keyExtractor={(item) => item.id.toString()}
                contentContainerStyle={{
                    padding: 20,
                    paddingBottom: 0,
                }}
                renderItem={({ item }) => {

                    return (
                        <View className="flex-row items-center justify-between bg-white mb-4 p-4 rounded-xl shadow-sm border border-gray-100">
                            <Image
                                source={{ uri: `http://10.100.102.9:8002/static/icons/${item.item_code}.png` }}
                                className="w-14 h-14 mr-3"
                                resizeMode="contain"
                            />
                            <View className="flex-1">
                                <Text className="text-right font-interSemi text-sm">{item.name}</Text>
                                <Text className="text-right text-xs text-gray-500 mt-1">
                                    {item.quantity} × ₪{item.price.toFixed(2)}
                                </Text>
                            </View>
                            <Text className="font-interBold text-black ml-2">
                                ₪{(item.price * parseInt(item.quantity)).toFixed(2)}
                            </Text>
                        </View>
                    );
                }}
                ListFooterComponent={
                    <BuyButton button_text="קנה עכשיו" handleAddToCart={handleBuyCart} />
                }

            />
            <BuyButton button_text="קנה" handleAddToCart={handleBuyCart}></BuyButton>
            <BottomNav />
        </View>

    );
}
