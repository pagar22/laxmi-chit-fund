import dayjs from "dayjs";
import { useEffect, useMemo, useState } from "react";
import { Dimensions } from "react-native";
import { Box, HStack, Text, VStack } from "@gluestack-ui/themed";
import { LineChart } from "react-native-chart-kit";
import { useSmallcaseIndexes } from "features/smallcases/hooks/useSmallcaseIndexes";

export const SmallcasePerformanceChart = ({ smallcase }) => {
  const [data, setData] = useState(undefined);
  const indexes = useSmallcaseIndexes(smallcase?.id);
  const colors = {
    kelly: "#FFD700",
    benchmark: "#40E0D0",
    smallcase: "#DC143C",
  };

  const chartData = useMemo(() => {
    if (indexes.isSuccess && indexes.data) {
      const data = indexes.data;
      const kellyData = [];
      const smallcaseData = [];
      const benchmarkData = [];
      const labels = new Set();

      Object.keys(data).forEach((date) => {
        labels.add(dayjs(date).format("MMM YY"));
        benchmarkData.push(data[date].benchmark);
        kellyData.push(data[date].kelly || 0);
        smallcaseData.push(data[date].smallcase);
      });

      return {
        labels: Array.from(labels),
        datasets: [
          // { data: kellyData, color: () => colors.kelly },
          { data: benchmarkData, color: () => colors.benchmark },
          { data: smallcaseData, color: () => colors.smallcase },
        ],
      };
    }
  }, [indexes.isSuccess]);

  useEffect(() => setData(chartData), [chartData]);

  return (
    <VStack>
      <Text size={"md"} bold>
        1Y Performance
      </Text>
      {data ? (
        <>
          <LineChart
            bezier
            data={data}
            width={Dimensions.get("window").width - 25}
            height={250}
            chartConfig={{
              color: () => `white`,
              labelColor: () => `white`,
              style: { borderRadius: 16 },
              propsForDots: { r: "0" },
              propsForBackgroundLines: { stroke: "none" },
              propsForLabels: { rotation: -45, fontSize: 12 },
            }}
            style={{ marginVertical: 16, borderRadius: 16 }}
          />
          <VStack
            p={12}
            mb={20}
            space={"md"}
            bg={"$trueGray700"}
            borderRadius={10}
          >
            <Text mb={-5} size={"lg"} bold>
              Legend
            </Text>
            <HStack justifyContent={"space-between"}>
              {/* <LegendDetail color={colors.kelly} text={"Kelly"} /> */}
              <LegendDetail color={colors.benchmark} text={"Benchmark"} />
              <LegendDetail color={colors.smallcase} text={"Smallcase"} />
            </HStack>
          </VStack>
        </>
      ) : (
        <></>
      )}
    </VStack>
  );
};

const LegendDetail = ({ color, text }) => {
  return (
    <HStack space={"md"}>
      <Box p={3} bg={color} />
      <Text>{text}</Text>
    </HStack>
  );
};
