import { createContext, useEffect, useState } from "react";
import { Platform } from "react-native";

import uuid from "react-native-uuid";
import * as SecureStore from "expo-secure-store";
import * as LocalAuthentication from "expo-local-authentication";
import { set } from "@gluestack-style/react";

export const AuthenticationContext = createContext(null);

export const AuthenticationContextProvider = ({ children }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const getDeviceId = async () => {
    const deviceId = await SecureStore.getItemAsync("deviceId");
    if (!deviceId) {
      const newDeviceId = uuid.v4();
      await SecureStore.setItemAsync("deviceId", newDeviceId);
      return newDeviceId;
    }
    return deviceId;
  };

  const getCustomToken = async (deviceId) => {
    console.debug(`🔐 Getting custom token for device ${deviceId}`);
    return "yo_token";
  };

  const getLocalAuthentication = async () => {
    const hasHardware = await LocalAuthentication.hasHardwareAsync();
    const hasEnrolled = await LocalAuthentication.isEnrolledAsync();
    if (hasHardware && hasEnrolled) {
      const result = await LocalAuthentication.authenticateAsync();
      if (result.success) {
        console.debug("🫶 Biometrics passed");
        return true;
      }
    } else {
      console.debug("👎 Biometrics not supported", hasHardware, hasEnrolled);
      return false;
    }
  };

  const authenticate = async () => {
    if (Platform.OS === "web") return;
    setIsLoading(true);
    const biometricsPassed = await getLocalAuthentication();
    if (biometricsPassed) {
      const deviceId = await getDeviceId();
      const customToken = await getCustomToken(deviceId);
      setIsAuthenticated(true);
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (!isAuthenticated) authenticate();
  }, []);

  return (
    <AuthenticationContext.Provider value={{ isAuthenticated, authenticate }}>
      {children}
    </AuthenticationContext.Provider>
  );
};

// export const useAuth = useContext(AuthenticationContext);
