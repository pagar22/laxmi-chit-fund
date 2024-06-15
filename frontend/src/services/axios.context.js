import { createContext, useMemo } from "react";
import axios from "axios";
import { Platform } from "react-native";
// import { Toastable } from "atoms/feedback/toast.atom";

export const AxiosContext = createContext(null);

export const AxiosContextProvider = ({ children }) => {
  const baseURL = "https://laxmi-chit-fund-xgqm3fv7ua-ew.a.run.app";
  const headers = {
    version: "1.0",
    platform: Platform.OS,
    accept: "application/json",
  };

  const client = useMemo(() => {
    const axiosClient = axios.create({ headers, baseURL });
    axiosClient.interceptors.response.use(
      (resp) => resp,
      (error) => {
        if (![401, 404, 423].includes(error?.response?.status)) {
          //   Toastable({
          //     bg: "red.600",
          //     fontColor: "lightText",
          //     body: getErrorMessage(error),
          //   });
        }
        return Promise.reject(error);
      }
    );
    return axiosClient;
  }, []);

  return (
    <AxiosContext.Provider value={{ client }}>{children}</AxiosContext.Provider>
  );
};
