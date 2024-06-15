import { Text, VStack } from "@gluestack-ui/themed";
import { NavigationPanel } from "theme/navigation-panel.component";
import { ScreenFrame } from "theme/screen-frame.component";

export const SettingsScreen = ({ navigation }) => {
  return (
    <ScreenFrame>
      <NavigationPanel navigation={navigation} />
      <VStack flex={1} px={10} space={"md"}>
        <Text size={"2xl"} bold>
          Trigger Cloud Functions
        </Text>
      </VStack>
    </ScreenFrame>
  );
};
