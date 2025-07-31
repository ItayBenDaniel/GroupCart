import { useState } from "react";
import { View, TextInput, Text, TouchableOpacity, Alert } from "react-native";
import { useRouter } from "expo-router";
import api from "../lib/axios";
export default function SignUpScreen() {
    const [email, setEmail] = useState("");
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [familyId, setFamily] = useState("")
    const router = useRouter();

    const handleSignUp = async () => {
        try {
            const res = await api.post("/users/signup", {
                username,
                email,
                password,
            });


            Alert.alert("נרשמת בהצלחה ✅");
            router.push("/login");

        } catch (err) {
            console.error(err);
            Alert.alert("שגיאה", "שם משתמש או סיסמה לא נכונים");
        }
        if (familyId) {
            try {
                await api.post(`/family/${familyId}/join?email=${email}`, {});
            } catch (err) {
                alert("התחברות למשפחה נכשלה");
            }
        } else {
            await api.post("/family", { name: `${username}'s Family` });
        }
    };

    return (
        <View className="flex-1 justify-center px-8 bg-white">

            <Text className="text-2xl font-bold mb-6 text-right">הרשמה</Text>
            <TextInput
                className="border rounded-md px-4 py-3 mb-4 text-right"
                placeholder="שם משתמש"
                onChangeText={setUsername}
                value={username}
            />
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
            <TextInput
                className="border rounded-md px-4 py-3 mb-6 text-right"
                placeholder="קוד משפחה"
                secureTextEntry
                onChangeText={setFamily}
                value={familyId}
            />

            <TouchableOpacity
                className="bg-orange-500 py-3 rounded-full"
                onPress={handleSignUp}
            >
                <Text className="text-white text-center font-bold">הרשמה</Text>
            </TouchableOpacity>

            <TouchableOpacity onPress={() => router.push("/login")}>
                <Text className="text-center text-app_orange mt-4">כבר נרשמת? התחבר</Text>
            </TouchableOpacity>
            {/* <BuyButton handleAddToCart={handleLogin} button_text="התחבר"></BuyButton> */}
        </View>
    );
}
