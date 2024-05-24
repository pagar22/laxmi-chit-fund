import { Heading, Text, VStack } from "@gluestack-ui/themed";
import { ScreenFrame } from "theme/screen-frame.component";

export const SmallcaseListScreen = () => {
  return (
    <ScreenFrame>
      <VStack p={5}>
        <Text px={10} size={"2xl"} bold>
          Smallcases
        </Text>
      </VStack>
    </ScreenFrame>
  );
};
