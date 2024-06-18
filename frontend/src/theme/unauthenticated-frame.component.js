import { useContext } from "react";
import { Dimensions } from "react-native";
import Ionicons from "@expo/vector-icons/Ionicons";
import {
  VStack,
  Text,
  Button,
  ButtonText,
  Spinner,
} from "@gluestack-ui/themed";
// internal
import { ScreenFrame } from "theme/screen-frame.component";
import { AuthenticationContext } from "services/authentication.context";

export const UnauthenticatedFrame = ({}) => {
  const { height } = Dimensions.get("screen");
  const { isLoading, authenticate } = useContext(AuthenticationContext);
  return (
    <ScreenFrame>
      <VStack
        flex={1}
        space={"sm"}
        h={height - 100}
        alignItems={"center"}
        justifyContent={"center"}
      >
        <Text size={"2xl"}>Verify yourself</Text>
        <Text size={"md"} textAlign={"center"} color={"$warmGray400"}>
          Use your biometrics to continue
        </Text>
        <Button
          size={"lg"}
          marginTop={20}
          action={"positive"}
          isDisabled={isLoading}
          onPress={authenticate}
        >
          <ButtonText mx={10}>Authenticate</ButtonText>
          <Ionicons size={24} color={"white"} name={"finger-print-outline"} />
        </Button>
        {isLoading && (
          <VStack position={"absolute"} bottom={150}>
            <Spinner size={"lg"} color={"$green400"} />
            <Text size={"md"} textAlign={"center"}>
              Authenticating...
            </Text>
            <Text size={"xs"}>This may take a few seconds</Text>
          </VStack>
        )}
      </VStack>
    </ScreenFrame>
  );
};
