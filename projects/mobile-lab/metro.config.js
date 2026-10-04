const {getDefaultConfig: nativeConfig, mergeConfig} = require('@react-native/metro-config');
const {getDefaultConfig: expoConfig} = require('expo/metro-config');
module.exports = mergeConfig(nativeConfig(__dirname), expoConfig(__dirname), {maxWorkers: 2});
