// screens/HomeScreen.tsx
import React, { useEffect, useState } from "react";
import { View, ScrollView } from "react-native";
import * as NavigationBar from "expo-navigation-bar";

import HeaderBar from "../components/HeaderBar";
import CategoriesBar from "../components/CategoryBar";
import ProductCard from "../components/ProductCard";
import ProductModal from "../components/ProductModal";
import useHomeScreenData, { StoreProduct } from "../hooks/useHomeScreenData";
import LottieView from "lottie-react-native";
import { checkTokenExpired } from "../lib/checkTokenExpired";
export default function HomeScreen() {
    const { username, randomProducts, loading } = useHomeScreenData();
    const [selectedProduct, setSelectedProduct] = useState<StoreProduct | null>(null);
    const [modalVisible, setModalVisible] = useState(false);
    const [categoryFilter, setCategoryFilter] = useState<string | null>(null);

    useEffect(() => {
        NavigationBar.setPositionAsync("absolute");
        NavigationBar.setBackgroundColorAsync("#ffffff01");

        checkTokenExpired();
    }, []);
    const handleProductPress = (product: StoreProduct) => {
        setSelectedProduct(product);
        setModalVisible(true);
    };

    if (loading) {
        return (
            <View className="flex-1 justify-center items-center bg-white">
                <LottieView
                    source={require("../assets/lottie/loading.json")}
                    autoPlay
                    loop
                    style={{ width: 300, height: 300 }}
                />
            </View>
        );
    }
    return (
        <View className="flex-1 relative bg-white mt-5">

            <ScrollView
                contentContainerStyle={{ paddingBottom: 100, paddingHorizontal: 16 }}
                showsVerticalScrollIndicator={false}
            >
                <HeaderBar name={username} />
                <CategoriesBar onCategorySelect={setCategoryFilter} />

                <View className="flex-row flex-wrap justify-between">
                    {(categoryFilter ? randomProducts.filter((p) => p.category === categoryFilter) : randomProducts)
                        .map((item, index) => (
                            <ProductCard
                                key={index}
                                image={{ uri: `http://10.100.102.23:8002/static/icons/${item.item_code}.png` }}
                                name={item.name}
                                quantity={item.quantity}
                                unit_of_measure={item.unit_of_measure}
                                price={item.price.toString()}
                                oldPrice={(item.price + 5).toString()}
                                onPress={() => handleProductPress(item)}
                            />
                        ))}
                </View>
            </ScrollView>
            <ProductModal
                visible={modalVisible}
                product={selectedProduct}
                onClose={() => setModalVisible(false)}
            />

        </View>
    );
}
