import { VStack } from "@gluestack-ui/themed";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
// internal
import { AccountsNavigator } from "features/accounts/accounts.navigator";
import { SmallcasesNavigator } from "features/smallcases/smallcases.navigator";
import { useContext } from "react";
import { AuthenticationContext } from "services/authentication.context";
import { UnauthenticatedFrame } from "theme/unauthenticated-frame.component";

const Stack = createNativeStackNavigator();

export const AppNavigator = () => {
  const { isAuthenticated } = useContext(AuthenticationContext);
  return isAuthenticated ? (
    <VStack flex={1} bg={"$trueGray900"}>
      <Stack.Navigator
        initialRouteName={"SmallcaseList"}
        screenOptions={{ headerShown: false }}
      >
        <Stack.Screen name={"Smallcases"} component={SmallcasesNavigator} />
        <Stack.Screen name={"Accounts"} component={AccountsNavigator} />
      </Stack.Navigator>
    </VStack>
  ) : (
    <UnauthenticatedFrame />
  );
};
