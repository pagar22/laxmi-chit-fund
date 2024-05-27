import { useContext } from "react";
import { useQuery } from "react-query";
// internal
import { formatDate } from "services/helpers";
import { AxiosContext } from "services/axios.context";

export const useSmallcaseIndexes = (id) => {
  const { client } = useContext(AxiosContext);
  return useQuery(
    [`smallcase-${id}-indexes`],
    () => {
      const start_date = formatDate("2016-01-01"); // inception
      const end_date = formatDate(); // today
      return client
        .get(`/smallcases/${id}/indexes?start_date=${start_date}`, {
          params: { start_date, end_date },
        })
        .then((resp) => resp.data);
    },
    {
      enabled: !!id,
      staleTime: 1000 * 60 * 5,
      refetchInterval: 1000 * 60,
      refetchOnWindowFocus: false,
    }
  );
};
