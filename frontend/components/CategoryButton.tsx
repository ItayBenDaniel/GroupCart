import { View, Text, TouchableOpacity, Image } from "react-native";

type Props = {
    label: string;
    icon: any;
    isActive?: boolean;
    onPress?: () => void;
};

export default function CategoryButton({ label, icon, isActive, onPress }: Props) {
    return (
        <TouchableOpacity
            onPress={onPress}
            className={`items-center justify-center px-3 py-2 mx-4 rounded-xl ${isActive ? "bg-app_orange" : "bg-gray-100"
                }`}
        >
            <Image source={icon} className="w-8 h-8 mb-1" />
            <Text
                className={`text-xs font-interSemi ${isActive ? "text-white" : "text-black"
                    }`}
            >
                {label}
            </Text>
        </TouchableOpacity>
    );
}
