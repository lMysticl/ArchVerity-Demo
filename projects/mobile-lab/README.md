# Expo / React Native laboratory

[Пошаговый запуск и общий маршрут демонстрации](../../docs/DEMO_RUNBOOK_RU.md#5-react-native--expo)
связывает эту лабораторию с первым finding, API, Impact и runtime evidence.

This is a real app, with a screen, interactions, console events, Metro config,
an index entry point, pinned dependencies and an npm lockfile. The package is
`com.archverity.demo`. Use a disposable emulator/simulator for device actions.

Node >=20.19.4 is required. Dependency versions follow the official
[Expo SDK 54 blank template](https://github.com/expo/expo/blob/sdk-54/templates/expo-template-blank/package.json).
Community CLI 20 matches React Native 0.81 according to its
[compatibility table](https://github.com/react-native-community/cli#compatibility).
They are fixed demo versions, not a claim to use the newest SDK.

```powershell
cd projects/mobile-lab
npm ci --ignore-scripts
npm run qa:verify
npm run start
```

`qa:verify` writes `work/qa-script-result.txt` with `RN_SCRIPT_OK`.
Expo starts its dev server. Stop it before running the alternative Metro action:
ArchVerity **React Native → Detect projects → mobile-lab → RN_METRO**.
`RN_METRO` uses the real installed `react-native` CLI; `RN_EXPO` uses Expo.
Press Stop and verify that the process actually exits before another start.

For **RN_BUNDLE**, select `android` or `ios`. The plugin writes a real JavaScript
bundle under `build/archflow-rn/index.<platform>.bundle`. `index.js` and the
community CLI are included specifically for this action. The terminal equivalent
for the Android sample is `npm run qa:verify` followed by `npm run bundle:android`.
No Android SDK/device is needed for this JavaScript bundle.

To keep a device session in its own Git checkout, run this from the suite root
before installing dependencies:

```powershell
python -B -X utf8 suite-support/prepare_project.py --project mobile-lab --output D:\CodexData\Temp\archverity-demo-mobile
cd D:\CodexData\Temp\archverity-demo-mobile
npm ci --ignore-scripts
```

The project's own `.gitignore` excludes dependencies, generated native projects,
device configuration and signing files in both the suite and the standalone copy.

Generate native projects before native commands, on the host used for that run:

```powershell
npm run prebuild
```

Expo's [prebuild workflow](https://docs.expo.dev/workflow/prebuild/) generates
`android/gradlew`, Android source and `ios/Podfile` from this app, using the SDK
54 template. It does not install pods because this script passes `--no-install`.
Run it in a disposable clone with neither native folder present. Do not run
`--clean` over native changes. Native directories, local device configuration and
any generated development signing material stay out of this public repository.
Installing/building/signing a native app is a separate operator-controlled step.

| ArchVerity command | Preparation / argument | Direct proof |
| --- | --- | --- |
| RN_SCRIPT | `qa:verify` | RN_SCRIPT_OK and the output file |
| RN_METRO | npm ci; no other process on 8081 | Real Metro process, `/status` reports running; Stop exits it |
| RN_EXPO | npm ci; select this project | Expo starts; QR/development URL appears; Stop exits it |
| RN_BUNDLE | `android` or `ios` | Nonempty bundle with the app's `ARCHVERITY_DEMO_CLICK` event |
| RN_ANDROID_RUN | Prebuild, SDK, JDK 17 supported by generated Android Gradle build, disposable emulator | Correct package is installed and this screen opens |
| RN_IOS_RUN | Prebuild on macOS, Xcode, pods, simulator | This app opens on the chosen simulator |
| GRADLE_TASK | Generated `android/gradlew`; choose `tasks`, then approved build task | Exit 0, correct native project and actual build artifact |
| COCOAPODS_INSTALL | macOS, CocoaPods, generated ios/Podfile | `pod install` exits 0 and generates Podfile.lock |
| IOS_DEVICES | macOS, Xcode | Actual `simctl` device JSON, not fabricated devices |
| ADB_DEVICES | Android platform-tools | Actual serial list; explicitly select one authorized disposable emulator |
| ADB_LOGCAT | That serial; press interaction button | `ARCHVERITY_DEMO_CLICK` appears for this app |
| ADB_REVERSE | Same serial; argument `8081` | adb reverse list contains tcp:8081 → tcp:8081 |
| ADB_RELOAD | Same serial, app open | Command opens the React Native developer menu; choose Reload there |
| ADB_INSTALL_APK | Actual generated debug APK and explicit install authority | `com.archverity.demo` exists on the selected emulator |
| ADB_UNINSTALL | `com.archverity.demo`; explicit uninstall authority | That package is absent afterwards |
| ADB_CLEAR_DATA | Same package; explicit clear-data authority | Device command succeeds; app restarts with baseline state |

The ADB_RELOAD action uses Android keyevent 82: the expected direct result is
the development menu. Automatic JS reload is not promised by that command.
The screen has an interaction counter and deliberate console-error button to
make log and recovery checks visible. No real payment/API credentials are used.

Windows/Linux cannot execute the iOS native commands. Simulator/device,
installation, app removal/data clearing, signing and a real macOS run remain
separate prerequisites. Record each as NOT RUN/BLOCKED until the corresponding
device/process/artifact is actually observed. The old workspace's `rn-qa` is
only a script-console fixture; use this app for all mobile runtime checks.
