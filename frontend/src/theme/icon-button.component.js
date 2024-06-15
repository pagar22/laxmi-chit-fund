import { Pressable } from "@gluestack-ui/themed";
import Ionicons from "@expo/vector-icons/Ionicons";

export const IconButton = ({ icon, onPress, ...props }) => {
  return (
    <Pressable
      {...props}
      p={5}
      onPress={onPress}
      rounded={"$full"}
      bg={"$trueGray700"}
    >
      <Ionicons name={icon} size={24} color={"white"} />
    </Pressable>
  );
};
