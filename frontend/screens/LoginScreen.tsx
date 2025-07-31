import { useState } from "react";
import { View, TextInput, Text, TouchableOpacity, Alert, Image } from "react-native";
import axios from "axios";
import { useRouter } from "expo-router";
import BuyButton from "../components/buttons/BuyButton";
import api from "../lib/axios";
import * as SecureStore from "expo-secure-store";
export default function LoginScreen() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const router = useRouter();

    const handleLogin = async () => {
        try {
            const res = await api.post("/users/login", {
                email,
                password,
            });

            const token = res.data.access_token;
            await SecureStore.setItemAsync("access_token", token);
            console.log("Token:", token);

            Alert.alert("התחברת בהצלחה ✅");
            router.replace("/");
        } catch (err) {
            console.error(err);
            Alert.alert("שגיאה", "שם משתמש או סיסמה לא נכונים");
        }
    };

    return (
        <View className="flex-1 justify-center px-8 bg-white">

            <Text className="text-2xl font-bold mb-6 text-right">התחברות</Text>

            <TextInput
                className="border rounded-md px-4 py-3 mb-4 text-right"
                placeholder="אימייל"
                onChangeText={setEmail}
                value={email}
            />
            <TextInput
                className="border rounded-md px-4 py-3 mb-6 text-right"
                placeholder="סיסמה"
                secureTextEntry
                onChangeText={setPassword}
                value={password}
            />

            <TouchableOpacity
                className="bg-orange-500 py-3 rounded-full"
                onPress={handleLogin}
            >
                <Text className="text-white text-center font-bold">התחבר</Text>
            </TouchableOpacity>
            {/* <BuyButton handleAddToCart={handleLogin} button_text="התחבר"></BuyButton> */}
        </View>
    );
}
