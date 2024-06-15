import { HStack } from "@gluestack-ui/themed";
import { IconButton } from "theme/icon-button.component";

export const NavigationPanel = ({ navigation }) => {
  return (
    <HStack px={10} pb={10}>
      <IconButton icon={"arrow-back"} onPress={() => navigation?.goBack()} />
    </HStack>
  );
};
