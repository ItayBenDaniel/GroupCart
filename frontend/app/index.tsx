import React from 'react';
import './global.css'
import { useEffect, useState } from "react";
import { Text, View } from 'react-native';
import HeaderBar from "../components/HeaderBar";
import PromoCard from "../components/PromoCard";
import CategoriesBar from "../components/CategoryBar";
import ProductCard from "../components/ProductCard";

import axios from "axios";

export default function App() {
  const [username, setUsername] = useState("");

  useEffect(() => {
    let isMounted = true;

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
      <ProductCard
        image={require("../assets/icons/milk.png")}
        name="שמנת לבישול 250 מ”ל תנובה"
        quantity="250 מ”ל"
        price="4.45"
        oldPrice="9.90"
        isFavorite
      />
    </View>
  );
}
