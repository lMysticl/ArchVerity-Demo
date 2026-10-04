import React, {useState} from 'react';
import {SafeAreaView, ScrollView, StyleSheet, Text, Pressable} from 'react-native';

export default function App() {
  const [count, setCount] = useState(0);
  const [status, setStatus] = useState('Ready for the first check');

  function verifyInteraction() {
    const next = count + 1;
    setCount(next);
    setStatus(`Interaction ${next} completed`);
    console.info(`ARCHVERITY_DEMO_CLICK ${next}`);
  }

  function verifyError() {
    setStatus('Intentional error recorded in the development console');
    console.error('ARCHVERITY_DEMO_INTENTIONAL_ERROR');
  }

  return (
    <SafeAreaView style={styles.page}>
      <ScrollView contentContainerStyle={styles.content}>
        <Text style={styles.eyebrow}>ARCHVERITY / MOBILE LAB</Text>
        <Text style={styles.title}>A real app for a repeatable check.</Text>
        <Text style={styles.description}>Use this screen to verify Metro, Expo, bundling, device logs, reload and native commands.</Text>
        <Text accessibilityRole="header" style={styles.counter}>{count}</Text>
        <Text accessibilityLiveRegion="polite" style={styles.status}>{status}</Text>
        <Pressable accessibilityRole="button" onPress={verifyInteraction} style={styles.button}>
          <Text style={styles.buttonText}>Run interaction check</Text>
        </Pressable>
        <Pressable accessibilityRole="button" onPress={verifyError} style={styles.secondary}>
          <Text style={styles.secondaryText}>Write an intentional error</Text>
        </Pressable>
        <Text style={styles.hint}>Package: com.archverity.demo. Clearing this disposable app's data resets local state; uninstalling it removes this app.</Text>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  page: {flex: 1, backgroundColor: '#10202D'},
  content: {padding: 28, gap: 22},
  eyebrow: {fontSize: 13, letterSpacing: 2, color: '#8EE3C1', fontWeight: '700'},
  title: {fontSize: 34, lineHeight: 40, color: '#FFFFFF', fontWeight: '700'},
  description: {fontSize: 17, lineHeight: 26, color: '#C7D5DF'},
  counter: {fontSize: 72, color: '#8EE3C1', fontWeight: '700'},
  status: {fontSize: 17, lineHeight: 25, color: '#FFFFFF'},
  button: {backgroundColor: '#8EE3C1', padding: 18, borderRadius: 12},
  buttonText: {color: '#10202D', fontSize: 16, fontWeight: '700', textAlign: 'center'},
  secondary: {borderColor: '#6A8090', borderWidth: 1, padding: 18, borderRadius: 12},
  secondaryText: {color: '#FFFFFF', fontSize: 16, textAlign: 'center'},
  hint: {fontSize: 13, lineHeight: 20, color: '#B5C4D0'},
});
