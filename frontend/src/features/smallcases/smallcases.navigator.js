import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { SmallcaseListScreen } from "features/smallcases/screens/smallcase-list.screen";

const Stack = createNativeStackNavigator();

export const SmallcasesNavigator = () => {
  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      <Stack.Screen name={"SmallcaseList"} component={SmallcaseListScreen} />
    </Stack.Navigator>
  );
};
