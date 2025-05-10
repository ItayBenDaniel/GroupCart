import { Slot, SplashScreen } from "expo-router";
import { useFonts } from "expo-font";
import { useEffect } from "react";

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

  return <Slot />;
}
