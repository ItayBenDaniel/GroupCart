import { ScrollView, View, Text } from "react-native";
import CategoryButton from "./CategoryButton";
import { useState } from "react";


const categories = [
    { label: "מוצרי חלב", icon: require("../assets/icons/milk.png") },
    { label: "מאפיה", icon: require("../assets/icons/bread.png") },
    { label: "קצביה", icon: require("../assets/icons/meat.png") },
    { label: "גבינות", icon: require("../assets/icons/cheese.png") },
    { label: "חטיפים", icon: require("../assets/icons/snack.png") },
];

export default function CategoriesBar() {
    const [selectedIndex, setSelectedIndex] = useState(0);

    return (
        <View className="mt-6">
            <View className="flex-row justify-between items-center px-4 mb-2">
                <Text className="text-orange-500 text-sm font-interSemi">ראה הכל</Text>
                <Text className="text-xl font-interBold">קטגוריות ראשיות</Text>
            </View>

            <ScrollView horizontal showsHorizontalScrollIndicator={false} className="px-3 mt-3">
                {categories.map((category, index) => (
                    <CategoryButton
                        key={index}
                        label={category.label}
                        icon={category.icon}
                        isActive={index === selectedIndex} // Example: highlight first category
                        onPress={() => setSelectedIndex(index)}

                    />
                ))}
            </ScrollView>
        </View>
    );
}
