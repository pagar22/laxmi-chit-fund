# Laxmi Chit Fund Frontend

Built using Expo 🐐 and React Native 🫶.

> This app is only meant to be build for native platforms (Android and iOS) and not the Web.

## Build

1. Install Dependencies

```
yarn install
```

2. Run locally

```
npx expo start --android --https
```

_Tip: Run with --i for ios_

Download an emulator on your laptop or the Expo app on your phone and scan the code to see the development app.

## Deploy

Build a preview version of the app (APK)

```
eas build -p android --profile preview
```

Build AAB (For PlayStore)

```
eas build -p android
```
