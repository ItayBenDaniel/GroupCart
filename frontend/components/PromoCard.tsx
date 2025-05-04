import { View, Text, Image } from "react-native";

type PromoCardProps = {
    title: string;
    image: any;
};

export default function PromoCard({ title, image }: PromoCardProps) {
    return (
        <View className="bg-orange-100 rounded-xl p-4 flex-row items-center space-x-4">
            <Image source={image} className="w-16 h-16 rounded-lg" />
            <Text className="text-base font-semibold text-orange-800">{title}</Text>
        </View>
    );
}
