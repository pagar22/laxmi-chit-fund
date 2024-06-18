import { createContext } from "react";
import { initializeApp } from "firebase/app";
import { initializeAuth, getAuth } from "firebase/auth";
import * as firebaseAuth from "firebase/auth";
import { getFirestore } from "firebase/firestore";
import { getFunctions } from "firebase/functions";
import AsyncStorage from "@react-native-async-storage/async-storage";

export const FirebaseContext = createContext(null);

export const FirebaseContextProvider = ({ children }) => {
  const config = {
    apiKey: "AIzaSyBtC4lY1S6u8VYJF79eTIKbtfQe1uLr_88",
    authDomain: "laxmi-chit-fund-letsgetit.firebaseapp.com",
    projectId: "laxmi-chit-fund-letsgetit",
    storageBucket: "laxmi-chit-fund-letsgetit.appspot.com",
    messagingSenderId: "55213090048",
    appId: "1:55213090048:web:f89a5c3e3ab50d215a7fe5",
    measurementId: "G-FR8ZB67FFG",
  };

  const getPersistentAuth = (app) => {
    try {
      return initializeAuth(app, {
        persistence: firebaseAuth.getReactNativePersistence(AsyncStorage),
      });
    } catch (error) {
      console.debug(`🥺 Auth config error, falling back`, error);
      return getAuth(app);
    }
  };

  const app = initializeApp(config);
  const auth = getPersistentAuth(app);
  const firestore = getFirestore(app);
  const functions = getFunctions(app, "europe-west1");

  return (
    <FirebaseContext.Provider
      value={{
        app,
        auth,
        config,
        firestore,
        functions,
      }}
    >
      {children}
    </FirebaseContext.Provider>
  );
};
