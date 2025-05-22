import { View } from "react-native";
import { Ionicons } from "@expo/vector-icons";
import { useState } from "react";
import { useRouter } from "expo-router";
import { TouchableOpacity, Text } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";

export default function BottomNav() {
    const [active, setActive] = useState("home");
    const router = useRouter();
    const insets = useSafeAreaInsets();

    return (
        <View className="flex-row z-10 justify-around items-center py-2 bg-white rounded-t-3xl border-t border-gray-200 absolute bottom-0 left-0 right-0" style={{ paddingBottom: insets.bottom || 12 }}>
            <NavItem icon="home" label="בית" active={active} setActive={setActive} onPress={() => router.push("/")} />
            <NavItem icon="cart" label="סל" active={active} setActive={setActive} onPress={() => router.push("/cart")} />
            <NavItem icon="person" label="פרופיל" active={active} setActive={setActive} onPress={() => { }} />
        </View>
    );
}

function NavItem({
    icon,
    label,
    active,
    setActive,
    onPress,
}: {
    icon: string;
    label: string;
    active: string;
    setActive: (val: string) => void;
    onPress: () => void;
}) {
    const isActive = active === icon;
    return (
        <TouchableOpacity
            onPress={() => {
                setActive(icon);
                onPress();
            }}
            className="items-center justify-center"
        >
            <Ionicons
                name={icon === "home" ? "home" : icon === "cart" ? "cart" : "person"}
                size={24}
                color={isActive ? "#f97316" : "#9ca3af"}
            />
            <Text className={`text-xs mt-1 ${isActive ? "text-orange-500" : "text-gray-400"}`}>
                {label}
            </Text>
        </TouchableOpacity>
    );
}
