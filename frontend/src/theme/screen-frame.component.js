import { Dimensions, Platform } from "react-native";
import { KeyboardAvoidingView, ScrollView, VStack } from "@gluestack-ui/themed";

export const ScreenFrame = ({ children }) => {
  const isWeb = Platform.OS === "web";
  const { height } = Dimensions.get("screen");

  return (
    <VStack
      flex={1}
      maxHeight={height}
      bg={"$trueGray900"}
      pt={isWeb ? 10 : 50}
      KeyboardAvoidingView={false}
    >
      <KeyboardAvoidingView
        flex={1}
        enabled={false}
        behavior={Platform.OS === "ios" ? "padding" : "height"}
      >
        <ScrollView showsVerticalScrollIndicator={false}>{children}</ScrollView>
      </KeyboardAvoidingView>
    </VStack>
  );
};
