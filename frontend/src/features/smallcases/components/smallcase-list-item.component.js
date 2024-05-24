import { HStack, Image, Text } from "@gluestack-ui/themed";

export const SmallcaseListItem = ({ smallcase }) => {
  return (
    <HStack
      p={8}
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
          source={{
            uri: "https://assets.smallcase.com/images/smallcases/160/SCNM_0025.png",
          }}
        />
        <Text size={"md"} bold>
          {smallcase.name}
        </Text>
      </HStack>
    </HStack>
  );
};
