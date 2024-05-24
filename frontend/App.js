import { GluestackUIProvider, Text } from "@gluestack-ui/themed";
import { config } from "@gluestack-ui/config";
import { StatusBar } from "expo-status-bar";

import { ScreenFrame } from "theme/screen-frame.component";
import { AppNavigator } from "navigation/app.navigator";
import { NavigationContainer } from "@react-navigation/native";
import { routes } from "navigation/route.config";

export default function App() {
  return (
    <GluestackUIProvider config={config} colorMode={"dark"}>
      <NavigationContainer linking={{ config: routes, enabled: true }}>
        <AppNavigator />
      </NavigationContainer>
      <StatusBar style={"light"} />
    </GluestackUIProvider>
  );
}
