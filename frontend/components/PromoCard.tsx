import { View, Text, Image, TouchableOpacity } from "react-native";

type PromoCardProps = {
    title: string;
    image: any;
};

export default function PromoCard({ title, image }: PromoCardProps) {
    return (
        <TouchableOpacity activeOpacity={0.9} className="w-2/3 bg-app_orange rounded-2xl gap-x-5 p-7 mt-5 mx-5 flex-row items-center ">
            <Image source={image} className="w-16 h-16 rounded-lg" />
            <Text className="text-xl text-white font-semibold flex-1 truncate ">{title}</Text>
        </TouchableOpacity>
    );
}
