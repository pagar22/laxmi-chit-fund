import { createContext } from "react";
import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";

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

  const app = initializeApp(config);
  const firestore = getFirestore(app);

  return (
    <FirebaseContext.Provider
      value={{
        app,
        config,
        firestore,
      }}
    >
      {children}
    </FirebaseContext.Provider>
  );
};
