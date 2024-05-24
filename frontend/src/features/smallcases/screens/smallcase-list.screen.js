import { FlatList, Text, VStack } from "@gluestack-ui/themed";
// internal
import { ScreenFrame } from "theme/screen-frame.component";
import { useSmallcases } from "features/smallcases/hooks/useSmallcases";
import { SmallcaseListItem } from "features/smallcases/components/smallcase-list-item.component";

export const SmallcaseListScreen = () => {
  const smallcases = useSmallcases();

  return (
    <ScreenFrame>
      <VStack flex={1} px={10}>
        <Text size={"2xl"} bold>
          Smallcases
        </Text>
        {smallcases?.data?.length > 0 && (
          <Text
            mb={5}
            size={"xs"}
          >{`${smallcases.data.length} Smallcases Found`}</Text>
        )}
        <FlatList
          py={12}
          contentContainerStyle={{ flexGrow: 1 }}
          data={smallcases.data}
          renderItem={({ item }) => (
            <SmallcaseListItem key={item.id} smallcase={item} />
          )}
        />
      </VStack>
    </ScreenFrame>
  );
};
