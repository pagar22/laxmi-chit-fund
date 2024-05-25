import { useContext } from "react";
import { useQuery } from "react-query";
import { AxiosContext } from "services/axios.context";

export const useSmallcase = (id) => {
  const { client } = useContext(AxiosContext);
  return useQuery([`smallcase-${id}`], () =>
    client.get(`/smallcases/${id}`).then((resp) => resp.data)
  );
};
