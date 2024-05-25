import { HStack, Image, Pressable, Text } from "@gluestack-ui/themed";

export const SmallcaseListItem = ({ smallcase, navigation }) => {
  return (
    <Pressable
      onPress={() => {
        navigation?.navigate("SmallcaseDetail", { id: smallcase?.id });
      }}
    >
      <HStack
        p={10}
        my={5}
        rounded={10}
        bg={"$trueGray800"}
        alignItems={"center"}
        justifyContent={"space-between"}
      >
        <HStack alignItems={"center"} space="md">
          <Image
            h={48}
            w={48}
            rounded={10}
            alt={"smallcase"}
            source={{ uri: smallcase?.pfp_url }}
          />
          <Text size={"md"} bold>
            {smallcase?.name}
          </Text>
        </HStack>
      </HStack>
    </Pressable>
  );
};
