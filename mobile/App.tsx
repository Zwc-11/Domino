import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native';

// Phase 0 shell. Navigation, API client, and screens arrive in Phase 4 (docs/PHASES.md).
export default function App() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>DOMINO</Text>
      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  title: {
    fontSize: 24,
    fontWeight: '600',
  },
});
