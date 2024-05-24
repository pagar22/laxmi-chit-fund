import "@expo/metro-runtime";
import { StatusBar } from "expo-status-bar";
import { config } from "@gluestack-ui/config";
import { GluestackUIProvider } from "@gluestack-ui/themed";
import { QueryClient, QueryClientProvider } from "react-query";
import { NavigationContainer } from "@react-navigation/native";
// internal
import { routes } from "navigation/route.config";
import { AppNavigator } from "navigation/app.navigator";
import { AxiosContextProvider } from "services/axios.context";

export default function App() {
  const queryClient = new QueryClient();

  return (
    <GluestackUIProvider config={config} colorMode={"dark"}>
      <QueryClientProvider client={queryClient}>
        <AxiosContextProvider>
          <NavigationContainer linking={{ config: routes, enabled: true }}>
            <AppNavigator />
          </NavigationContainer>
          <StatusBar style={"light"} />
        </AxiosContextProvider>
      </QueryClientProvider>
    </GluestackUIProvider>
  );
}
