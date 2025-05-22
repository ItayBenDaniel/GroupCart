import React, { useEffect, useState } from "react";

import './global.css'
import { View } from 'react-native';
import HomeScreen from '../screens/HomeScreen';

export default function App() {

  return (
    <View className="flex-1 relative bg-white">
      <HomeScreen></HomeScreen>
    </View>
  );
}
