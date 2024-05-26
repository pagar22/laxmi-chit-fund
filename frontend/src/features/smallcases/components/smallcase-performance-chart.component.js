import { Box, Text, VStack } from "@gluestack-ui/themed";
import dayjs from "dayjs";
import { VictoryAxis, VictoryChart, VictoryLegend, VictoryLine } from "victory";

export const SmallcasePerformanceChart = ({}) => {
  const benchmark = [
    { day: "2021-01-01", index: 100 },
    { day: "2021-01-02", index: 105 },
    { day: "2021-01-03", index: 114 },
    { day: "2021-01-04", index: 115 },
    { day: "2021-01-05", index: 125 },
  ];
  const smallcase = [
    { day: "2021-01-01", index: 100 },
    { day: "2021-01-02", index: 102 },
    { day: "2021-01-03", index: 116 },
    { day: "2021-01-04", index: 120 },
    { day: "2021-01-05", index: 128 },
  ];
  const kelly = [
    { day: "2021-01-01", index: 100 },
    { day: "2021-01-02", index: 107 },
    { day: "2021-01-03", index: 118 },
    { day: "2021-01-04", index: 122 },
    { day: "2021-01-05", index: 132 },
  ];
  const indexes = {
    kelly: kelly,
    smallcase: smallcase,
    benchamrk: benchmark,
  };
  const props = { x: "day", y: "index" };

  return (
    <VStack>
      <Text size={"md"} bold>
        Performance
      </Text>
      <VictoryChart>
        <VictoryAxis
          fixLabelOverlap
          tickCount={10}
          style={{ axis: { stroke: "#fff" }, tickLabels: { fill: "#fff" } }}
          tickFormat={(data) => dayjs(data, "DD.MM.YYYY").format("MMM-YY")}
        />
        <VictoryAxis
          dependentAxis
          fixLabelOverlap
          tickCount={10}
          style={{
            axis: { stroke: "#fff" },
            tickLabels: { fill: "#fff" },
            grid: { stroke: "#fff", strokeDasharray: "5 20" },
          }}
        />
        <VictoryLine
          {...props}
          data={indexes.benchamrk}
          style={{ data: { stroke: "#fff" } }}
        />
        <VictoryLine
          {...props}
          data={indexes.smallcase}
          style={{ data: { stroke: "#fb7185" } }}
        />
        <VictoryLine
          {...props}
          data={indexes.kelly}
          style={{ data: { stroke: "#6ee7b7" } }}
        />
      </VictoryChart>
      <Box h={50}>
        <VictoryLegend
          gutter={20}
          width={"100%"}
          height={"100%"}
          orientation={"horizontal"}
          style={{ border: { stroke: "#fff" }, labels: { fill: "#fff" } }}
          data={[
            { name: "Benchmark", symbol: { fill: "#fff" } },
            { name: "Smallcase", symbol: { fill: "#fb7185" } },
            { name: "Kelly Optimal", symbol: { fill: "#6ee7b7" } },
          ]}
        />
      </Box>
    </VStack>
  );
};
