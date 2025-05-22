import { View, Text, TouchableOpacity } from "react-native";

type Props = {
    button_text: string,
    handleAddToCart?: () => void;
};
export default function BuyButton({
    button_text,
    handleAddToCart
}: Props) {

    return (
        <View className="px-4 mt-10 pb-6">
            <TouchableOpacity onPress={handleAddToCart} className="bg-app_orange py-3 rounded-full">
                <Text className="text-white font-interBold text-center text-base">{button_text}</Text>
            </TouchableOpacity>
        </View>
    );
}
