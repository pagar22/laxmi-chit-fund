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
      const now = new Date();
      const end_date = formatDate(now); // today
      const start_date = formatDate(now.setFullYear(now.getFullYear() - 1)); // 1 year ago
      return client
        .get(`/smallcases/${id}/indexes?start_date=${start_date}`, {
          params: { start_date, end_date },
        })
        .then((resp) => resp.data);
    },
    {
      enabled: !!id,
      staleTime: Infinity,
      refetchOnWindowFocus: false,
      refetchInterval: 1000 * 60 * 5,
    }
  );
};
