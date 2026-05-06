import { StatusBar } from 'expo-status-bar';
import { StyleSheet, View, SafeAreaView, Text } from 'react-native';
import Inbox from './Inbox';

export default function App() {
  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>MagicBell Inbox</Text>
      </View>
      <Inbox />
      <StatusBar style="auto" />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  header: {
    height: 60,
    backgroundColor: '#fff',
    justifyContent: 'center',
    alignItems: 'center',
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
    paddingTop: 10,
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: 'bold',
  },
});
