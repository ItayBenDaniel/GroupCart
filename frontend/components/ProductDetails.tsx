import { View, Text, Image, ScrollView, TouchableOpacity } from "react-native";
import { Ionicons } from "@expo/vector-icons";
import axios from "axios";
import { Alert } from "react-native";
import BuyButton from "./buttons/BuyButton"

type Props = {
    product_id: number;
    image: any;
    name: string;
    quantity: string;
    price: string;
    unit_of_measure: string;
    oldPrice?: string;
    isFavorite?: boolean;
    onClose?: () => void;
};
export default function ProductDetails({
    product_id,
    image,
    name,
    quantity,
    price,
    unit_of_measure,
    oldPrice,
    isFavorite = false,
    onClose,
}: Props) {
    console.log("PRODUCT ID2 ", product_id)

    const storeOptions = [
        { name: "קינגסטור ", price: "7.40", image: "kingstore" },
        { name: "שופרסל דיל", price: "7.40", image: "kingstore" },
        { name: "רמי לוי", price: "7.30", image: "rami_levi" },
    ];
    const handleAddToCart = async () => {
        console.log("PRODUCT ID3 ", product_id)
        try {
            const res = await axios.post("http://10.100.102.9:8002/cart/", {
                store_product_id: product_id,
                quantity: 1,
            });

            Alert.alert("המוצר נוסף לסל 🎉");
        } catch (err) {
            console.error("Failed to add to cart:", err);
            Alert.alert("שגיאה", "לא ניתן להוסיף את המוצר לסל");
        }
    };
    return (
        <View className="flex-1 bg-white ">
            <TouchableOpacity onPress={onClose} className="absolute top-10 left-4 z-50">
                <Ionicons name="close" size={28} color="black" />
            </TouchableOpacity>
            {/* Top image and back icon */}
            <View className="bg-gray-100 rounded-b-3xl pb-6 pt-10 px-4 items-center">
                <Image source={image} className="w-40 h-40 mt-2" resizeMode="contain" />
            </View>

            {/* Title + price */}
            <View className="px-5 pt-10 gap-y-3">
                <Text className="text-3xl font-interBold text-right">{name}</Text>
                <View className="flex-row  rtl:space-x-reverse gap-x-2">
                    <Text className="text-2xl font-interBold">₪ {price}</Text>
                    <Text className="text-m line-through text-gray-400">₪ {oldPrice}</Text>
                </View>
            </View>

            {/* Store slider */}
            <ScrollView horizontal showsHorizontalScrollIndicator={false} className="mt-4 px-4 ">
                {storeOptions.map((store, i) => (
                    <TouchableOpacity
                        key={i}
                        className="bg-gray-100 px-10 py-2 rounded-xl mr-5 items-center justify-start "
                        style={{ alignSelf: "flex-start" }} // key line: this avoids height stretching
                    >
                        <Text className="font-interSemi text-xs text-center">{store.name}</Text>
                        <Text className="text-black font-interBold mt-1 text-sm">₪ {store.price}</Text>
                        <Image
                            source={{ uri: `http://10.100.102.9:8002/static/icons/${store.image}.png` }}
                            className="w-20 h-20 object-contain mt-2"
                        />
                    </TouchableOpacity>
                ))}
            </ScrollView>

            {/* Add to cart button */}

            <BuyButton button_text="הוסף לסל" handleAddToCart={handleAddToCart}></BuyButton>
        </View>
    );
}
