import { HStack, Box, Pressable } from "@gluestack-ui/themed";
import Ionicons from "@expo/vector-icons/Ionicons";

export const NavigationPanel = ({ navigation }) => {
  return (
    <HStack px={10} pb={10}>
      <Pressable
        p={5}
        rounded={"$full"}
        bg={"$trueGray700"}
        onPress={() => navigation?.goBack()}
      >
        <Ionicons name="arrow-back" size={24} color="white" />
      </Pressable>
    </HStack>
  );
};
