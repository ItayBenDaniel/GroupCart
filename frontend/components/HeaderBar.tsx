import { View, Text, TouchableOpacity } from "react-native";
import { Ionicons } from "@expo/vector-icons";

type HeaderProps = {
    name?: string; // optional
};

export default function HeaderBar({ name = "" }: HeaderProps) {
    return (
        <View className="flex-col mt-3" >
            <View className="flex-row items-center justify-between mx-3">
                <TouchableOpacity className="bg-gray-100 rounded-full p-2">
                    <Ionicons name="menu" size={24} color="black" />
                </TouchableOpacity>
                <TouchableOpacity className="bg-gray-100 rounded-full p-2">
                    <Ionicons name="search" size={24} color="black" />
                </TouchableOpacity>
            </View>
            <View className="mt-5 mx-5 items-end">
                <Text className="text-xl font-bold">שלום {name}!</Text>
                <Text className="text-sm text-gray-500 font-bold">בוא נתחיל לקנות :)</Text>
            </View>
        </View>
    );
}
