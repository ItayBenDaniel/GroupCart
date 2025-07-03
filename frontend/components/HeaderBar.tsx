import { useRef, useState } from "react";
import { View, Text, TextInput, TouchableOpacity, Modal, Pressable, Keyboard } from "react-native";
import { Ionicons } from "@expo/vector-icons";

type HeaderBarProps = {
    name?: string;
    searchTerm: string;
    setSearchTerm: (text: string) => void;
};
export default function HeaderBar({ name = "",
    searchTerm,
    setSearchTerm,
}: HeaderBarProps) {
    const [isSearchActive, setIsSearchActive] = useState(false);
    const inputRef = useRef<TextInput>(null);

    const openSearch = () => {
        setIsSearchActive(true);
        setTimeout(() => inputRef.current?.focus(), 50);
    };

    return (
        <View className="flex-col mt-3">
            {/* Top row with icon */}
            <View className="flex-row justify-between items-center mx-5 mb-2">
                <TouchableOpacity onPress={openSearch} className="w-6">
                    <Ionicons
                        name="search"
                        size={24}
                        color="gray"
                        style={{ opacity: isSearchActive ? 0 : 1 }}
                    />
                </TouchableOpacity>
                <View className="items-end">
                    <Text className="text-2xl font-bold">שלום {name}!</Text>
                    <Text className="text-m text-gray-500 font-bold">בוא נתחיל לקנות :)</Text>
                </View>
            </View>

            {/* Search Modal */}
            <Modal transparent animationType="fade" visible={isSearchActive}>
                <Pressable
                    onPress={() => setIsSearchActive(false)}
                    className="absolute inset-0 bg-black opacity-40"
                />
                <View className="absolute top-10 left-0 right-0 px-6">
                    <View className="bg-white rounded-full flex-row items-center px-4 py-2 shadow-md">
                        <Ionicons name="search" size={20} color="gray" />
                        <TextInput
                            ref={inputRef}
                            placeholder="חפש מוצר..."
                            value={searchTerm}
                            onChangeText={setSearchTerm}
                            onSubmitEditing={() => {
                                Keyboard.dismiss();
                                setIsSearchActive(false);
                            }}
                            className="flex-1 px-3 text-right"
                            placeholderTextColor="gray"
                        />
                        {searchTerm !== "" && (
                            <TouchableOpacity onPress={() => setSearchTerm("")} className="ml-2">
                                <Ionicons name="close-circle" size={20} color="gray" />
                            </TouchableOpacity>
                        )}
                        <TouchableOpacity onPress={() => setIsSearchActive(false)}>
                            <Ionicons name="close" size={20} color="gray" />
                        </TouchableOpacity>
                    </View>
                </View>
            </Modal>
        </View>
    );
}
