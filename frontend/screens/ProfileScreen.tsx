import { View, Text, TouchableOpacity } from "react-native";
import { useEffect, useState } from "react";
import { useRouter } from "expo-router";
import * as SecureStore from "expo-secure-store";
import api from "../lib/axios";
import useUserData from "../hooks/useUserData";

export default function ProfileScreen() {
    const user = useUserData();
    const router = useRouter();

    useEffect(() => {
        // const fetchUser = async () => {
        //     const token = await SecureStore.getItemAsync("token");
        //     if (token) {
        //         api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
        //         const res = await api.get("/users/me");
        //         setUsername(res.data.username);
        //     }
        // };
        // fetchUser();
    }, []);

    return (
        <View className="flex-1 bg-white px-6 pt-16">
            <Text className="text-2xl font-bold text-right mb-6">שלום, {user?.user?.username}</Text>

            <TouchableOpacity
                //onPress={() => router.push("/purchases")}
                className="bg-gray-100 rounded-xl px-4 py-5 mb-4 shadow-sm"
            >
                <Text className="text-right text-lg font-semibold">הצג רכישות קודמות</Text>
            </TouchableOpacity>

            <TouchableOpacity
                //onPress={() => router.push("/family")}
                className="bg-gray-100 rounded-xl px-4 py-5 mb-4 shadow-sm"
            >
                <Text className="text-right text-lg font-semibold">חברי המשפחה</Text>
            </TouchableOpacity>

            <TouchableOpacity
                onPress={async () => {
                    await SecureStore.deleteItemAsync("access_token");
                    router.replace("/signup");
                }}
                className="bg-orange-500 rounded-full py-4 mt-10"
            >
                <Text className="text-white font-bold text-center text-lg">התנתק</Text>
            </TouchableOpacity>
        </View>
    );
}
