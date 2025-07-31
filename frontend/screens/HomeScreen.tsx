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
import useUserData from "../hooks/useUserData";

export default function HomeScreen() {
    const { randomProducts, loading, likedIds, toggleLike } = useHomeScreenData();
    const user = useUserData();
    const [username, setUsername] = useState("");

    const [selectedProduct, setSelectedProduct] = useState<StoreProduct | null>(null);
    const [modalVisible, setModalVisible] = useState(false);
    const [categoryFilter, setCategoryFilter] = useState<string | null>(null);
    const [searchTerm, setSearchTerm] = useState("");

    useEffect(() => {
        // if (user?.user?.username) {
        //     setUsername(user.user.username);
        // } else {
        //     setUsername("");
        // }
        NavigationBar.setPositionAsync("absolute");
        NavigationBar.setBackgroundColorAsync("#ffffff01");

        checkTokenExpired();
    }, []);
    const handleProductPress = (product: StoreProduct) => {
        setSelectedProduct(product);
        setModalVisible(true);
        setSearchTerm("");
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
                contentContainerStyle={{ paddingBottom: 100, paddingHorizontal: 10 }}
                showsVerticalScrollIndicator={false}
            >
                <HeaderBar name={user?.user?.username} searchTerm={searchTerm} setSearchTerm={setSearchTerm} />

                <CategoriesBar onCategorySelect={(category) => {
                    setCategoryFilter(category);
                    setSearchTerm("");
                }} />

                <View className="flex-row flex-wrap justify-between">
                    {(categoryFilter
                        ? randomProducts.filter((p) => p.category === categoryFilter)
                        : randomProducts
                    )
                        .filter((p) =>
                            p.name.toLowerCase().includes(searchTerm.toLowerCase())
                        )
                        .map((item, index) => {
                            const hasPromotion =
                                item.promotion_price !== null &&
                                item.promotion_price !== undefined &&
                                typeof item.promotion_price === "number";

                            const finalPrice: number = hasPromotion ? item.promotion_price! : item.price;
                            const oldPrice: number | null = hasPromotion ? item.price : null;

                            const sale: number | null =
                                hasPromotion && item.price
                                    ? Math.round(((item.price - item.promotion_price!) / item.price) * 100)
                                    : null;
                            return (
                                <ProductCard
                                    key={index}
                                    image={{ uri: `http://10.100.102.23:8002/static/icons/${item.item_code}.png` }}
                                    name={item.name}
                                    quantity={item.quantity}
                                    unit_of_measure={item.unit_of_measure}
                                    price={finalPrice.toFixed(2)}
                                    oldPrice={oldPrice ? oldPrice.toFixed(2) : undefined}
                                    sale={sale ? sale.toString() : undefined}
                                    onPress={() => handleProductPress(item)}
                                    liked={likedIds.has(item.id)}
                                    onToggleLike={() => toggleLike(item.id)}
                                />
                            );
                        })}
                </View>
            </ScrollView>
            <ProductModal
                visible={modalVisible}
                product={selectedProduct}
                onClose={() => setModalVisible(false)

                }
            />

        </View>
    );
}
