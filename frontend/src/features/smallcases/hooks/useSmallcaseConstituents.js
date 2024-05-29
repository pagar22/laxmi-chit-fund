import { useContext } from "react";
import { useQuery } from "react-query";
import { AxiosContext } from "services/axios.context";

export const useSmallcaseConstituents = (id, date) => {
  const { client } = useContext(AxiosContext);
  return useQuery(
    [`smallcase-${id}-constituents`],
    () => {
      return client
        .get(`/smallcases/${id}/constituents?date=${date}`)
        .then((resp) => resp.data);
    },
    {
      staleTime: Infinity,
      refetchOnWindowFocus: false,
      refetchInterval: 1000 * 60 * 5,
    }
  );
};
