import {
  KeyboardAvoidingView,
  SafeAreaView,
  VStack,
} from "@gluestack-ui/themed";
import { Dimensions, Platform } from "react-native";

export const ScreenFrame = ({ children }) => {
  const { height } = Dimensions.get("screen");
  const isWeb = Platform.OS === "web";

  return (
    <SafeAreaView flex={1} pt={isWeb ? 0 : 40} bg={"$warmGray800"}>
      <KeyboardAvoidingView
        flex={1}
        enabled={false}
        behavior={Platform.OS === "ios" ? "padding" : "height"}
      >
        <VStack flex={1} maxHeight={height} KeyboardAvoidingView={false}>
          {children}
        </VStack>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
};
