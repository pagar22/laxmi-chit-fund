import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { AdminPanelScreen } from "features/accounts/screens/admin-panel.screen";

const Stack = createNativeStackNavigator();

export const AccountsNavigator = () => {
  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      <Stack.Screen name={"AdminPanel"} component={AdminPanelScreen} />
    </Stack.Navigator>
  );
};
