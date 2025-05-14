import React from 'react';
import './global.css'
import { useEffect, useState } from "react";
import { ScrollView, FlatList, Text, View } from 'react-native';
import HeaderBar from "../components/HeaderBar";
import PromoCard from "../components/PromoCard";
import CategoriesBar from "../components/CategoryBar";
import ProductCard from "../components/ProductCard";
import * as NavigationBar from "expo-navigation-bar";

import axios from "axios";

export default function App() {
  const [username, setUsername] = useState("");
  const [selectedLiked, setSelectedLike] = useState(0);

  const products = [
    {
      name: "שמנת לבישול 250 מ”ל תנובה",
      quantity: "250 מ”ל",
      price: "4.45",
      oldPrice: "9.90",
      image: require("../assets/icons/milk.png"),
    },
    {
      name: "חלב 1 ליטר תנובה",
      quantity: "1 ליטר",
      price: "5.99",
      oldPrice: "8.50",
      image: require("../assets/icons/bread.png"),
    },
    {
      name: "חלב 1 ליטר תנובה",
      quantity: "1 ליטר",
      price: "5.99",
      oldPrice: "8.50",
      image: require("../assets/icons/bread.png"),
    },
    {
      name: "חלב 1 ליטר תנובה",
      quantity: "1 ליטר",
      price: "5.99",
      oldPrice: "8.50",
      image: require("../assets/icons/bread.png"),
    },
    {
      name: "חלב 1 ליטר תנובה",
      quantity: "1 ליטר",
      price: "5.99",
      oldPrice: "8.50",
      image: require("../assets/icons/bread.png"),
    },
    {
      name: "חלב 1 ליטר תנובה",
      quantity: "1 ליטר",
      price: "5.99",
      oldPrice: "8.50",
      image: require("../assets/icons/bread.png"),
    },
    {
      name: "חלב 1 ליטר תנובה",
      quantity: "1 ליטר",
      price: "5.99",
      oldPrice: "8.50",
      image: require("../assets/icons/bread.png"),
    },
    {
      name: "חלב 1 ליטר תנובה",
      quantity: "1 ליטר",
      price: "5.99",
      oldPrice: "8.50",
      image: require("../assets/icons/bread.png"),
    },
    {
      name: "חלב 1 ליטר תנובה",
      quantity: "1 ליטר",
      price: "5.99",
      oldPrice: "8.50",
      image: require("../assets/icons/bread.png"),
    },
    {
      name: "חלב 1 ליטר תנובה",
      quantity: "1 ליטר",
      price: "5.99",
      oldPrice: "8.50",
      image: require("../assets/icons/bread.png"),
    },
    {
      name: "חלב 1 ליטר תנובה",
      quantity: "1 ליטר",
      price: "5.99",
      oldPrice: "8.50",
      image: require("../assets/icons/bread.png"),
    },
    // add more...
  ];
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

    return () => {
      isMounted = false;
    };
  }, []);

  return (
    <View>

      <HeaderBar name={username} />
      <PromoCard title="10% הנחה על כל הקטגוריה!" image={require("../assets/images/react-logo.png")} />
      <CategoriesBar />
      <FlatList
        data={products}
        keyExtractor={(_, index) => index.toString()}
        numColumns={2}
        columnWrapperStyle={{ justifyContent: "space-between", paddingHorizontal: 16 }}
        contentContainerStyle={{ paddingBottom: 100 }}
        renderItem={({ item }) => (
          <ProductCard
            image={item.image}
            name={item.name}
            quantity={item.quantity}
            price={item.price}
            oldPrice={item.oldPrice}
          />
        )}
      />

    </View>
  );
}
