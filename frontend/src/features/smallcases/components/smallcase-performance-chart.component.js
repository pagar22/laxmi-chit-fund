import { useEffect, useState } from "react";
import { Box, Text, VStack } from "@gluestack-ui/themed";
import dayjs from "dayjs";
import {
  VictoryAxis,
  VictoryChart,
  VictoryLegend,
  VictoryLine,
  VictoryTooltip,
  createContainer,
} from "victory";
import { useSmallcaseIndexes } from "features/smallcases/hooks/useSmallcaseIndexes";

export const SmallcasePerformanceChart = ({ smallcase }) => {
  const [data, setData] = useState([]);
  const indexes = useSmallcaseIndexes(smallcase?.id);

  useEffect(() => {
    if (indexes.isSuccess) {
      const indexesData = indexes.data;
      const values = Object.keys(indexesData).map((day) => ({
        day,
        smallcase: indexesData[day].smallcase,
        benchmark: indexesData[day].benchmark,
        kelly: indexesData[day].kelly,
      }));
      setData(values);
    }
  }, [indexes.isSuccess]);

  // const data = [
  //   { kelly: 100, smallcase: 100, benchmark: 100, day: "2021-01-01" },
  //   { kelly: 107, smallcase: 102, benchmark: 105, day: "2021-01-02" },
  //   { kelly: 118, smallcase: 116, benchmark: 114, day: "2021-01-03" },
  //   { kelly: 122, smallcase: 120, benchmark: 115, day: "2021-01-04" },
  //   { kelly: 132, smallcase: 125, benchmark: 122, day: "2021-01-05" },
  // ];
  const props = { x: "day" };

  const VictoryZoomVoronoiContainer = createContainer("voronoi", "cursor");

  return (
    <VStack>
      <Text size={"md"} bold>
        Performance
      </Text>
      <VictoryChart
        containerComponent={
          <VictoryZoomVoronoiContainer
            cursorDimension="x"
            cursorComponent={<line stroke={"#fff"} strokeWidth={2} />}
            labels={({ datum }) =>
              `Benchmark: ${datum.benchmark}\nSmallcase: ${
                datum.smallcase
              }\nKelly Optimal: ${datum.kelly}\n As of: ${dayjs(
                datum.day
              ).format("MMM DD, YYYY")}`
            }
            labelComponent={
              <VictoryTooltip
                style={{ fill: "#fff" }}
                flyoutStyle={{
                  stroke: "#fff",
                  fill: "#404040",
                }}
              />
            }
          />
        }
      >
        <VictoryAxis
          fixLabelOverlap
          tickCount={10}
          style={{ axis: { stroke: "#fff" }, tickLabels: { fill: "#fff" } }}
          tickFormat={(data) => dayjs(data, "DD.MM.YYYY").format("YYYY")}
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
          data={data}
          y={"benchmark"}
          style={{ data: { stroke: "#fff" } }}
        />
        <VictoryLine
          {...props}
          data={data}
          y={"smallcase"}
          style={{ data: { stroke: "#fb7185" } }}
        />
        <VictoryLine
          {...props}
          data={data}
          y={"kelly"}
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
