import { ScrollView, View, Text } from "react-native";
import CategoryButton from "./CategoryButton";
import { useState } from "react";


type Props = {
    onCategorySelect: (category: string | null) => void;
};

export default function CategoriesBar({ onCategorySelect }: Props) {
    const [selectedIndex, setSelectedIndex] = useState<number | null>(null);

    const categories = [
        { label: "בשר ודגים", value: "בשר ודגים", image: "meat" },
        { label: "פירות וירקות", value: "פירות וירקות", image: "fruits" },
        { label: "חלב וגבינות", value: "חלב וגבינות", image: "milk" },
        { label: "מאפים ולחמים", value: "מאפים ולחמים", image: "bread" },
        { label: "ממתקים וחטיפים", value: "ממתקים וחטיפים", image: "sweets" },
        { label: "משקאות", value: "משקאות", image: "drinks" },
        { label: "תבלינים ואפייה", value: "תבלינים ואפייה", image: "spices" },
        { label: "קוסמטיקה", value: "קוסמטיקה וטיפוח אישי", image: "cosmetics" },
    ];

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
                        icon={{ uri: `http://10.100.102.23:8002/static/icons/${category.image}.png` }} // optional
                        isActive={index === selectedIndex}
                        onPress={() => {
                            const isSelected = selectedIndex === index;
                            setSelectedIndex(isSelected ? null : index);
                            onCategorySelect(isSelected ? null : category.value);
                        }}
                    />
                ))}
            </ScrollView>
        </View>
    );
}
