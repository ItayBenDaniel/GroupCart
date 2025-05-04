import React from 'react';
import { Text, View } from 'react-native';
import HeaderBar from "../components/HeaderBar";
import PromoCard from "../components/PromoCard";

export default function HomeScreen() {
    return (
        <View className="flex-1 pt-5 px-4 bg-white">
            <HeaderBar name="איתי" />
            <PromoCard title='test' image={require("../assets/images/favicon.png")} />
            {/* PromoCards, CategoryList, ProductGrid go here next */}
        </View>
    );
}
