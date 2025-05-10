import { useEffect, useState } from "react";
import { Text, View } from 'react-native';
import HeaderBar from "../components/HeaderBar";
import PromoCard from "../components/PromoCard";
import CategoriesBar from "../components/CategoryBar";

import axios from "axios";

export default function HomeScreen() {
    const [username, setUsername] = useState("");

    useEffect(() => {
        axios.get("http://10.100.102.9:8002/users/users/1") // replace with correct ID and IP
            .then((res) => {
                setUsername(res.data.username);
                console.log(res.data.username);
            })
            .catch((err) => {
                console.error("Failed to fetch user", err);
            });
    }, []);

    return (
        <View>
            <HeaderBar name={username} />
            <PromoCard title="10% הנחה על כל הקטגוריה!" image={require("../assets/images/react-logo.png")} />
            <CategoriesBar />
        </View>
    );
}
