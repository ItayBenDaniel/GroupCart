import { View, Text, Image, TouchableOpacity } from "react-native";
import { Ionicons } from "@expo/vector-icons";

type Props = {
    image: any;
    name: string;
    quantity: string;
    price: string;
    oldPrice?: string;
    isFavorite?: boolean;
};

export default function ProductCard({
    image,
    name,
    quantity,
    price,
    oldPrice,
    isFavorite = false,
}: Props) {
    return (
        <View className="w-[48%] bg-white rounded-xl p-3 mb-4 shadow-sm border border-gray-100">
            {/* Top row: discount + favorite */}
            <View className="flex-row justify-between items-center mb-2">
                <View className="bg-orange-100 px-2 py-1 rounded-md">
                    <Text className="text-[10px] text-orange-600 font-interSemi">הנחה 50%</Text>
                </View>
                <TouchableOpacity>
                    <Ionicons
                        name={isFavorite ? "heart" : "heart-outline"}
                        size={16}
                        color={isFavorite ? "red" : "gray"}
                    />
                </TouchableOpacity>
            </View>

            {/* Image */}
            <Image source={image} className="w-full h-24 object-contain mb-2" resizeMode="contain" />

            {/* Title */}
            <Text className="text-xs text-right leading-4 font-interSemi">{name}</Text>
            <Text className="text-[10px] text-gray-500 text-right mt-1">{quantity}</Text>

            {/* Price */}
            <View className="flex-row items-center justify-end mt-1 space-x-2 rtl:space-x-reverse">
                <Text className="text-base font-interBold text-black">₪ {price}</Text>
                {oldPrice && (
                    <Text className="text-xs text-gray-400 line-through">₪ {oldPrice}</Text>
                )}
            </View>
        </View>
    );
}
