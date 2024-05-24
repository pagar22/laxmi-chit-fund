import { useContext } from "react";
import { useQuery } from "react-query";
import { AxiosContext } from "services/axios.context";

export const useSmallcases = () => {
  const { client } = useContext(AxiosContext);
  return useQuery(
    ["smallcases"],
    () => client.get("/smallcases/").then((resp) => resp.data),
    { refetchInterval: 1000 * 60, staleTime: 1000 * 60 * 5 }
  );
};
