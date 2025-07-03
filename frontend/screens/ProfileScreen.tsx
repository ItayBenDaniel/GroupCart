import { View, Text, TouchableOpacity, ScrollView, Alert } from "react-native";
import { useState } from "react";
import { useRouter } from "expo-router";
import * as SecureStore from "expo-secure-store";
import api from "../lib/axios";
import useUserData from "../hooks/useUserData";
import dayjs from 'dayjs';
import { Picker } from "@react-native-picker/picker";

export default function ProfileScreen() {
    const user = useUserData();
    const router = useRouter();
    const [showPurchases, setShowPurchases] = useState(false);
    const [showFamily, setShowFamily] = useState(false);
    const [purchases, setPurchases] = useState<any[]>([]);
    const [familyMembers, setFamilyMembers] = useState<any[]>([]);
    const [radius, setRadius] = useState(5);
    const [familyName, setFamilyName] = useState<string | null>(null);

    const togglePurchases = async () => {
        if (!showPurchases) {
            try {
                const res = await api.get("/purchases/");
                setPurchases(res.data);
            } catch (err) {
                console.error("Failed to fetch purchases:", err);
            }
        }
        setShowPurchases(!showPurchases);
    };
    const toggleFamily = async () => {
        if (!showFamily) {
            try {
                const res = await api.get("/family/me");
                setFamilyMembers(res.data.members);
                setFamilyName(res.data.name || `משפחה #${res.data.id}`);
            } catch (err) {
                console.error("Failed to fetch Family:", err);
            }
        }
        setShowFamily(!showFamily);
    };

    const updateRadius = async () => {
        try {

            const res = await api.post(`/users/radius?radius=${radius}`);
            Alert.alert("רדיוס החיפוש עודכן בהצלחה", "");
            console.log("res is :", res.data)
        } catch (err) {
            console.error("Updating user radius failed:", err);
            alert("שגיאה בעדכון נתונים.");
        }
    };
    return (
        <View className="flex-1 bg-white px-6 pt-16">
            <Text className="text-2xl font-bold text-right mb-6">שלום, {user?.user?.username}</Text>

            <TouchableOpacity
                onPress={togglePurchases}
                className="bg-gray-100 rounded-xl px-4 py-5 mb-4 shadow-sm"
            >
                <Text className="text-right text-lg font-semibold">
                    {showPurchases ? "הסתר רכישות" : "הצג רכישות קודמות"}
                </Text>
            </TouchableOpacity>
            {showPurchases && (
                <ScrollView className="bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 mb-4">
                    {purchases.length === 0 ? (
                        <Text className="text-right text-sm text-gray-500">אין רכישות קודמות</Text>
                    ) : (
                        purchases.map((purchase, index) => (
                            <View key={index} className="mb-3">
                                <Text className="text-right text-m font-bold text-orange-600 mb-1">
                                    רכישה #{index + 1}
                                </Text>
                                <Text className="text-right text-m font-bold text-orange-600 mb-1">
                                    הרכישה התבצעה ב #{dayjs(purchase.purchased_at).format("DD/MM/YYYY HH:mm")}
                                </Text>
                                {purchase.items.map((item: any, i: number) => (
                                    <Text key={i} className="text-right text-s text-gray-700 mb-2">
                                        {item.product.name} — {item.quantity} יח'
                                    </Text>
                                ))}
                            </View>
                        ))
                    )}
                </ScrollView>
            )}

            <TouchableOpacity
                onPress={toggleFamily}
                className="bg-gray-100 rounded-xl px-4 py-5 mb-4 shadow-sm"
            >
                <Text className="text-right text-lg font-semibold">
                    {showFamily ? "הסתר חברי משפחה" : "הצג חברי משפחה"}
                </Text>
            </TouchableOpacity>

            {showFamily && (

                <View className="bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 mb-4">
                    {familyName && (
                        <Text className="text-right text-lg font-bold text-gray-800 mb-2">
                            {`את/ה שייך/ת ל${familyName}`}
                        </Text>
                    )}
                    {familyMembers.length === 0 ? (
                        <Text className="text-right text-sm text-gray-500">אין חברים במשפחה</Text>
                    ) : (
                        familyMembers.map((member, index) => (
                            <View key={index} className="mb-2">
                                <Text className="text-right text-m font-bold text-orange-600">{member.username}</Text>
                                <Text className="text-right text-s text-gray-700">{member.email}</Text>
                            </View>
                        ))
                    )}
                </View>
            )}
            <View className="bg-gray-100 rounded-xl px-4 py-5 mb-4 shadow-sm">
                <Text className="text-right text-lg font-semibold mb-2">בחר רדיוס (בק"מ):</Text>
                <Picker
                    selectedValue={radius}
                    onValueChange={(value) => setRadius(value)}
                    mode="dropdown"
                    style={{ height: 50 }}
                >
                    {[1, 2, 5, 10, 15, 20, 50, 100].map((km) => (
                        <Picker.Item key={km} label={`${km} ק"מ`} value={km} />
                    ))}
                </Picker>

                <TouchableOpacity
                    onPress={updateRadius}
                    className="bg-blue-500 rounded-full py-3 mt-4"
                >
                    <Text className="text-white font-bold text-center text-lg">עדכן רדיוס חיפוש</Text>
                </TouchableOpacity>
            </View>
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
