import React from 'react';
import './global.css'
import { Stack } from "expo-router";

import HomeScreen from '../screens/HomeScreen';

export default function App() {
  return (
    <>
      <Stack.Screen options={{ headerShown: false }} />
      <HomeScreen />
    </>
  );
}