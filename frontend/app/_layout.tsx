import { Slot, SplashScreen, Stack } from "expo-router";
import { View } from "react-native"
import { useFonts } from "expo-font";
import { useEffect } from "react";
import BottomNav from "../components/BottomNav";

export default function RootLayout() {
  const [loaded] = useFonts({
    Inter: require("../assets/fonts/Inter-Regular.ttf"),
    InterSemi: require("../assets/fonts/Inter-SemiBold.ttf"),
    InterBold: require("../assets/fonts/Inter-Bold.ttf"),
  });

  useEffect(() => {
    if (loaded) {
      SplashScreen.hideAsync();
    }
  }, [loaded]);

  if (!loaded) return null;

  return (
    <>
      <View className="flex-1 bg-white" >

        <Stack screenOptions={{ headerShown: false }} />
        <BottomNav />
      </View>

    </>
  );
}
