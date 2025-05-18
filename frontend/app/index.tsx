import React from 'react';
import './global.css'
import { useEffect, useState } from "react";
import { ScrollView, FlatList, Text, View } from 'react-native';
import HeaderBar from "../components/HeaderBar";
import PromoCard from "../components/PromoCard";
import CategoriesBar from "../components/CategoryBar";
import ProductCard from "../components/ProductCard";
import * as NavigationBar from "expo-navigation-bar";
import { Modal } from "react-native";
import ProductDetails from "../components/ProductDetails"; // create this if you haven’t

import axios from "axios";
type StoreProduct = {
  id: number;
  name: string;
  price: number;
  quantity: string
  item_code: string;
  original_price?: number;
  unit_of_measure: string;
  // Add any other expected fields from the backend
};


export default function App() {
  const [username, setUsername] = useState("");
  const [selectedLiked, setSelectedLike] = useState(0);
  const [randomProducts, setRandomProducts] = useState<StoreProduct[]>([]);
  const [selectedProduct, setSelectedProduct] = useState<StoreProduct | null>(null);
  const [modalVisible, setModalVisible] = useState(false);
  useEffect(() => {
    let isMounted = true;
    NavigationBar.setPositionAsync("absolute");
    NavigationBar.setBackgroundColorAsync("#ffffff01");
    axios.get("http://10.100.102.9:8002/users/users/1")
      .then((res) => {
        if (isMounted) {
          setUsername(res.data.username);
          console.log(res.data.username);
        }
      })
      .catch((err) => {
        if (isMounted) {
          console.error("Failed to fetch user", err);
        }
      });

    axios.get("http://10.100.102.9:8002/store_products/random/10")
      .then((res) => {
        if (isMounted) {
          setRandomProducts(res.data);
        }
      })
      .catch((err) => console.error("Failed to fetch products", err));

    return () => {
      isMounted = false;
    };
  }, []);

  const handleProductPress = (product: StoreProduct) => {
    setSelectedProduct(product);
    setModalVisible(true);
  };
  return (
    <View>

      <HeaderBar name={username} />
      <PromoCard title="10% הנחה על כל הקטגוריה!" image={require("../assets/images/react-logo.png")} />
      <CategoriesBar />
      <FlatList
        data={randomProducts}
        keyExtractor={(_, index) => index.toString()}
        numColumns={2}
        columnWrapperStyle={{ justifyContent: "space-between", paddingHorizontal: 16 }}
        contentContainerStyle={{ paddingBottom: 100 }}
        renderItem={({ item }) => (
          <ProductCard
            image={{ uri: `http://10.100.102.9:8002/static/icons/${item.item_code}.png` }}
            name={item.name}
            quantity={item.quantity}
            unit_of_measure={item.unit_of_measure}
            price={item.price.toString()}
            oldPrice={(item.price + 5).toString()}
            onPress={() => handleProductPress(item)}
          />
        )}
      />
      <Modal visible={modalVisible} animationType="slide" onRequestClose={() => setModalVisible(false)}>
        {selectedProduct && (
          <ProductDetails
            image={{ uri: `http://10.100.102.9:8002/static/icons/${selectedProduct.item_code}.png` }}
            name={selectedProduct.name}
            quantity={selectedProduct.quantity}
            unit_of_measure={selectedProduct.unit_of_measure}
            price={selectedProduct.price.toString()}
            oldPrice={(selectedProduct.price + 5).toString()}
            onClose={() => setModalVisible(false)}
          />
        )}
      </Modal>
    </View>
  );
}
