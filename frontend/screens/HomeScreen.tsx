// screens/HomeScreen.tsx
import React, { useEffect, useState } from "react";
import { FlatList, View, ActivityIndicator } from "react-native";
import * as NavigationBar from "expo-navigation-bar";

import HeaderBar from "../components/HeaderBar";
import PromoCard from "../components/PromoCard";
import CategoriesBar from "../components/CategoryBar";
import ProductCard from "../components/ProductCard";
import BottomNav from "../components/BottomNav";
import ProductModal from "../components/ProductModal";
import useHomeScreenData, { StoreProduct } from "../hooks/useHomeScreenData";
import LottieView from "lottie-react-native";
import { checkTokenExpired } from "../lib/checkTokenExpired";
export default function HomeScreen() {
    const { username, randomProducts, loading } = useHomeScreenData();
    const [selectedProduct, setSelectedProduct] = useState<StoreProduct | null>(null);
    const [modalVisible, setModalVisible] = useState(false);

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
        <View className="flex-1 relative bg-white">
            <HeaderBar name={username} />
            {/* <PromoCard title="10% הנחה על כל הקטגוריה!" image={require("../assets/images/react-logo.png")} /> */}
            <CategoriesBar />
            <FlatList
                data={randomProducts}
                keyExtractor={(_, index) => index.toString()}
                numColumns={2}
                contentContainerStyle={{ paddingBottom: 100, paddingHorizontal: 16 }}
                columnWrapperStyle={{ justifyContent: "space-between" }}
                renderItem={({ item }) => (
                    <ProductCard
                        image={{ uri: `http://192.168.68.52:8002/static/icons/${item.item_code}.png` }}
                        name={item.name}
                        quantity={item.quantity}
                        unit_of_measure={item.unit_of_measure}
                        price={item.price.toString()}
                        oldPrice={(item.price + 5).toString()}
                        onPress={() => handleProductPress(item)}
                    />
                )}
            />
            <ProductModal
                visible={modalVisible}
                product={selectedProduct}
                onClose={() => setModalVisible(false)}
            />

        </View>
    );
}
