import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { SettingsScreen } from "features/accounts/screens/settings.screen";

const Stack = createNativeStackNavigator();

export const AccountsNavigator = () => {
  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      <Stack.Screen name={"Settings"} component={SettingsScreen} />
    </Stack.Navigator>
  );
};
