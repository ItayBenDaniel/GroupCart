import { View, Text, Image, TouchableOpacity } from "react-native";
import { useState } from "react";

import { Ionicons } from "@expo/vector-icons";

type Props = {
    image: any;
    name: string;
    quantity: string;
    price: string;
    unit_of_measure: string;
    oldPrice?: string;
    liked?: boolean;
    sale: string
    onToggleLike?: () => void;
    onPress?: () => void;
};

export default function ProductCard({
    image,
    name,
    quantity,
    price,
    unit_of_measure,
    oldPrice,
    liked = false,
    sale,
    onToggleLike,
    onPress,
}: Props) {

    return (
        <TouchableOpacity onPress={onPress} activeOpacity={0.9} className="w-[48%] bg-white rounded-xl p-3 mb-4 mt-3 shadow-sm border border-gray-100">
            {/* Top row: discount + favorite */}
            <View className="flex-row-reverse justify-between items-center mb-2">
                {/* Heart icon always on right */}
                <TouchableOpacity onPress={onToggleLike}>
                    <Ionicons
                        name={liked ? "heart" : "heart-outline"}
                        size={20}
                        color={liked ? "red" : "gray"}
                    />
                </TouchableOpacity>

                {/* Sale badge or placeholder to preserve spacing */}
                {sale !== "0" ? (
                    <View className="bg-orange-100 px-2 py-1 rounded-md">
                        <Text className="text-sm text-orange-600 font-interSemi">הנחה {sale}%</Text>
                    </View>
                ) : (
                    <View className="w-16" /> // same width as badge to keep spacing
                )}
            </View>

            {/* Image */}
            <Image source={image} className="w-full h-24 object-contain mb-2" resizeMode="contain" />

            {/* Title */}
            <Text className="text-xs text-right leading-4 font-interSemi">{name}</Text>
            <Text className="text-[10px] text-gray-500 text-right mt-1">{unit_of_measure}</Text>

            {/* Price */}
            <View className="flex-row items-center justify-end mt-1 space-x-2 gap-x-2 rtl:space-x-reverse">
                <Text className="text-base font-interBold text-black">₪ {price}</Text>
                {oldPrice && (
                    <Text className="text-xs text-gray-400 line-through">₪ {oldPrice}</Text>
                )}
            </View>
        </TouchableOpacity>
    );
}
