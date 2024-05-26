import { useState } from "react";
import {
  Divider,
  FlatList,
  HStack,
  Image,
  Switch,
  Text,
  VStack,
} from "@gluestack-ui/themed";
// internal
import { ScreenFrame } from "theme/screen-frame.component";
import { NavigationPanel } from "theme/navigation-panel.component";
import { camelToTitle, formatDate, rounded } from "services/helpers";
import { useSmallcase } from "features/smallcases/hooks/useSmallcase";
import { useSmallcaseConstituents } from "features/smallcases/hooks/useSmallcaseConstituents";

export const SmallcaseDetailScreen = ({ navigation, route }) => {
  const { id } = route.params;
  const now = formatDate();
  const [date, setDate] = useState(now);
  const [kelly, setKelly] = useState(false);

  const smallcase = useSmallcase(id);
  const constituents = useSmallcaseConstituents(id, date);

  return (
    <ScreenFrame>
      <NavigationPanel navigation={navigation} />
      <VStack flex={1} px={10} space={"md"}>
        <VStack>
          <HStack justifyContent={"space-between"}>
            <Text size={"2xl"} bold>
              {smallcase.data?.name}
            </Text>
            <Image
              h={40}
              w={40}
              rounded={20}
              source={{ uri: smallcase.data?.pfp_url }}
            />
          </HStack>
          <Text size={"2xs"} color={"$primary200"}>
            {smallcase.data?.id}
          </Text>
          <Text size={"2xs"}>{smallcase.data?.description}</Text>
        </VStack>
        <HStack mt={10} space={"xl"}>
          {smallcase.data?.investment_strategies?.map((strategy, index) => (
            <Text
              p={6}
              key={index}
              size={"sm"}
              rounded={10}
              color={"black"}
              bg={"$primary200"}
            >
              {camelToTitle(strategy)}
            </Text>
          ))}
        </HStack>
        <HStack mt={10} justifyContent={"space-between"}>
          <Text size={"md"} bold>
            Constituents
          </Text>
          <HStack space={"xl"}>
            <Text color={"$tertiary300"} bold>
              Kelly
            </Text>
            <Switch
              value={kelly}
              onValueChange={setKelly}
              trackColor={{ true: "$tertiary300", false: "$trueGray300" }}
            />
          </HStack>
        </HStack>
        <HStack justifyContent={"space-between"} space={"xl"}>
          <Text size={"md"}>Name</Text>
          <Text size={"md"}>{`Weightage (%)`}</Text>
        </HStack>
        <Divider bg={"white"} />
        <FlatList
          data={constituents.data?.constituents}
          renderItem={({ item, index }) => (
            <>
              <HStack p={6} space={"xl"} justifyContent={"space-between"}>
                <Text size={"sm"} isTruncated>
                  {item.smallcase_name}
                </Text>
                <Text
                  size={"sm"}
                  textAlign={"right"}
                  color={kelly && "$tertiary300"}
                >
                  {`${rounded(
                    kelly
                      ? item.kelly_weightage || 0
                      : item.original_weightage * 100
                  )} %`}
                </Text>
              </HStack>
              <Divider my={12} />
            </>
          )}
        />
      </VStack>
    </ScreenFrame>
  );
};
