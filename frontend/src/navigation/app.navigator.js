import { VStack } from "@gluestack-ui/themed";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
// internal
import { SmallcasesNavigator } from "features/smallcases/smallcases.navigator";

const Stack = createNativeStackNavigator();

export const AppNavigator = () => {
  //   const { initialised } = useContext(AxiosContext);
  return (
    true && (
      <VStack flex={1} bg={"$warmGray800"}>
        <Stack.Navigator screenOptions={{ headerShown: false }}>
          <Stack.Screen name={"Smallcases"} component={SmallcasesNavigator} />
        </Stack.Navigator>
      </VStack>
    )
  );
  //   ) : (
  //     <SplashFrame />
  //   );
};
