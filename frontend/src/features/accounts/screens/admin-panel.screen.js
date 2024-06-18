import { useContext, useState } from "react";
import { Dimensions } from "react-native";
import {
  FlatList,
  Pressable,
  Spinner,
  Text,
  VStack,
} from "@gluestack-ui/themed";
import { httpsCallable } from "firebase/functions";
import Ionicons from "@expo/vector-icons/Ionicons";
// internal
import { FirebaseContext } from "services/firebase.context";
import { ScreenFrame } from "theme/screen-frame.component";
import { NavigationPanel } from "theme/navigation-panel.component";

const { width } = Dimensions.get("screen");

const TriggerFunctionPanel = ({ item }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [triggerState, setTriggerState] = useState("untriggered");

  const invokeFunction = async () => {
    console.log(`🚀 Invoking ${item.name}`);
    return item
      .function()
      .then((result) => {
        setIsLoading(false);
        setTriggerState("success");
        return result.data;
      })
      .catch((error) => {
        console.error(error);
        setIsLoading(false);
        setTriggerState("failure");
      });
  };

  return (
    <Pressable
      m={5}
      p={10}
      h={100}
      rounded={10}
      w={width / 2.3}
      bg={"$trueGray700"}
      disabled={isLoading}
      onPress={invokeFunction}
      $disabled-bg={"$trueGray800"}
    >
      <VStack alignItems={"center"}>
        <Text fontSize={14} textAlign={"center"} fontWeight={900} isTruncated>
          {item?.name}
        </Text>
        <Text mb={8} fontSize={10} textAlign={"center"} color={"$warmGray400"}>
          Tap to trigger
        </Text>
        {isLoading ? (
          <Spinner />
        ) : triggerState === "failure" ? (
          <Ionicons name={"close-circle-outline"} size={32} color={"red"} />
        ) : triggerState === "success" ? (
          <Ionicons name={"checkmark-circle"} size={32} color={"green"} />
        ) : (
          <Ionicons name={"rocket-outline"} size={32} color={"yellow"} />
        )}
      </VStack>
    </Pressable>
  );
};

export const AdminPanelScreen = ({ navigation }) => {
  const { functions } = useContext(FirebaseContext);
  const cloudFunctions = [
    {
      name: "Calculate Kelly",
      function: httpsCallable(functions, "cf-model-kelly"),
    },
    {
      name: "Calculate Indexes",
      function: httpsCallable(functions, "cf-model-indexes"),
    },
    {
      name: "Scrape Tickers",
      function: httpsCallable(functions, "cf-scrape-tickers"),
    },
    {
      name: "Scrape Candlesticks",
      function: httpsCallable(functions, "cf-scrape-candlesticks"),
    },
  ];

  return (
    <ScreenFrame>
      <NavigationPanel navigation={navigation} />
      <VStack flex={1} px={10} space={"md"}>
        <Text size={"2xl"} bold>
          Trigger Cloud Functions
        </Text>
        <FlatList
          numColumns={2}
          contentContainerStyle={{ flexGrow: 1 }}
          data={cloudFunctions}
          renderItem={({ item }) => <TriggerFunctionPanel item={item} />}
        />
      </VStack>
    </ScreenFrame>
  );
};
