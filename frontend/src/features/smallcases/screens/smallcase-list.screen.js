import { FlatList, HStack, Text, VStack } from "@gluestack-ui/themed";
// internal
import { IconButton } from "theme/icon-button.component";
import { ScreenFrame } from "theme/screen-frame.component";
import { useAuthentication } from "services/authentication.context";
import { useSmallcases } from "features/smallcases/hooks/useSmallcases";
import { SmallcaseListItem } from "features/smallcases/components/smallcase-list-item.component";

export const SmallcaseListScreen = ({ navigation }) => {
  const smallcases = useSmallcases();
  const { user } = useAuthentication();

  return (
    <ScreenFrame>
      <VStack flex={1} px={10}>
        <HStack justifyContent={"space-between"} alignItems={"center"}>
          <Text size={"2xl"} bold>
            Smallcases
          </Text>
          {user?.claims?.is_admin && (
            <IconButton
              icon={"rocket-outline"}
              onPress={() => {
                navigation.navigate("Accounts", { screen: "Settings" });
              }}
            />
          )}
        </HStack>
        {smallcases?.data?.length > 0 && (
          <Text
            mb={5}
            size={"xs"}
          >{`${smallcases.data.length} Smallcases`}</Text>
        )}
        <FlatList
          py={12}
          showsVerticalScrollIndicator={false}
          contentContainerStyle={{ flexGrow: 1 }}
          data={smallcases.data}
          renderItem={({ item }) => (
            <SmallcaseListItem
              key={item.id}
              smallcase={item}
              navigation={navigation}
            />
          )}
        />
      </VStack>
    </ScreenFrame>
  );
};
