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
import { SmallcasePerformanceChart } from "features/smallcases/components/smallcase-performance-chart.component";

export const SmallcaseDetailScreen = ({ navigation, route }) => {
  const { id } = route.params;
  const [kelly, setKelly] = useState(false);

  const now = formatDate();
  const smallcase = useSmallcase(id);
  const constituents = useSmallcaseConstituents(id, now);

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
              alt={"smallcase-pfp"}
              source={
                smallcase.data?.pfp_url
                  ? { uri: smallcase.data?.pfp_url }
                  : { uri: "none" }
              }
            />
          </HStack>
          <Text size={"xs"} color={"$primary200"}>
            {smallcase.data?.id}
          </Text>
          <Text size={"xs"}>{smallcase.data?.description}</Text>
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
        <HStack mt={10} justifyContent={"space-between"} alignItems={"center"}>
          <Text size={"md"} bold>
            Constituents
          </Text>
          <HStack space={"xl"} alignItems={"center"}>
            <Text color={kelly ? "#9FE394" : "#fff"} bold>
              Kelly
            </Text>
            <Switch
              value={kelly}
              onValueChange={setKelly}
              trackColor={{ true: "#9FE394", false: "$trueGray300" }}
            />
          </HStack>
        </HStack>
        <HStack justifyContent={"space-between"} space={"xl"}>
          <Text size={"md"}>Name</Text>
          <Text size={"md"}>{`Weightage (%)`}</Text>
        </HStack>
        <Divider bg={"#fff"} />
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
                  color={kelly ? "#9FE394" : "#fff"}
                >
                  {`${rounded(
                    kelly
                      ? item.adjusted_kelly_weightage * 100 || 0
                      : item.original_weightage * 100
                  )} %`}
                </Text>
              </HStack>
              <Divider my={12} />
            </>
          )}
        />
        {smallcase.isSuccess && (
          <SmallcasePerformanceChart smallcase={smallcase.data} />
        )}
      </VStack>
    </ScreenFrame>
  );
};
