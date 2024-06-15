import { useContext } from "react";
import Ionicons from "@expo/vector-icons/Ionicons";
import { VStack, Text, Button, ButtonText } from "@gluestack-ui/themed";
// internal
import { ScreenFrame } from "theme/screen-frame.component";
import { AuthenticationContext } from "services/authentication.context";

export const UnauthenticatedFrame = ({ children }) => {
  const { isLoading, authenticate } = useContext(AuthenticationContext);
  return (
    <ScreenFrame>
      <VStack
        h={500}
        flex={1}
        space={"xs"}
        alignItems={"center"}
        justifyContent={"center"}
      >
        <Text size={"2xl"}>Verify yourself</Text>
        <Text size={"md"} textAlign={"center"} color={"$warmGray400"}>
          Use your biometrics to continue
        </Text>
        <Button
          marginTop={20}
          action={"positive"}
          variant={"outline"}
          isLoading={isLoading}
          onPress={authenticate}
        >
          <ButtonText>Authenticate</ButtonText>
          <Ionicons
            size={24}
            marginLeft={10}
            color={"green"}
            name={"finger-print-outline"}
          />
        </Button>
      </VStack>
    </ScreenFrame>
  );
};
