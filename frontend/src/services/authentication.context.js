import { createContext, useContext, useEffect, useState } from "react";
import { Platform } from "react-native";
import uuid from "react-native-uuid";
import * as SecureStore from "expo-secure-store";
import * as LocalAuthentication from "expo-local-authentication";
import { signInWithCustomToken } from "firebase/auth";
// internal
import { getRandomString } from "services/helpers";
import { FirebaseContext } from "services/firebase.context";
import { httpsCallable } from "firebase/functions";

export const AuthenticationContext = createContext(null);

export const AuthenticationContextProvider = ({ children }) => {
  const { auth, functions } = useContext(FirebaseContext);

  const [user, setUser] = useState(undefined);
  const [isLoading, setIsLoading] = useState(false);

  const getDeviceId = async () => {
    const deviceId = await SecureStore.getItemAsync("deviceId");
    if (!deviceId) {
      const newDeviceId = getRandomString();
      await SecureStore.setItemAsync("deviceId", newDeviceId);
      return newDeviceId;
    }
    return deviceId;
  };

  const getDevicePassword = async () => {
    const devicePassword = await SecureStore.getItemAsync("devicePassword");
    if (!devicePassword) {
      const newDevicePassword = uuid.v4();
      await SecureStore.setItemAsync("devicePassword", newDevicePassword);
      return newDevicePassword;
    }
    return devicePassword;
  };

  const getCustomToken = async (deviceId, password) => {
    console.debug(`🔐 Getting custom token for ${deviceId}`);
    const payload = { deviceId, password };
    const authCF = httpsCallable(functions, "firebase-auth");
    return authCF(payload)
      .then((result) => result.data)
      .catch((error) => console.error(error));
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

    const biometricsPassed = await getLocalAuthentication();
    if (biometricsPassed) {
      setIsLoading(true);
      const deviceId = await getDeviceId();
      const password = await getDevicePassword();
      const customToken = await getCustomToken(deviceId, password);
      signInWithCustomToken(auth, customToken)
        .then(async (result) => {
          console.debug("🔑 User signed in", result.user.uid);
          const claims = await result.user.getIdTokenResult();
          const user = Object.assign({}, result.user, claims);
          setUser(user);
          setIsLoading(false);
        })
        .catch((error) => {
          console.error(error);
          setIsLoading(false);
        });
    }
  };

  useEffect(() => {
    if (!user) authenticate();
  }, []);

  return (
    <AuthenticationContext.Provider
      value={{ user, isLoading, isAuthenticated: !!user, authenticate }}
    >
      {children}
    </AuthenticationContext.Provider>
  );
};
