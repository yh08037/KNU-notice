import React from "react";
import {
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  StatusBar
} from "react-native";

export default function App() {
  return (
    <View style={styles.container}>
      <StatusBar barStyle="dark-content" />
      <View style={styles.halfContainer}>
        <Text style={styles.textTitle}>KNU Notice</Text>
      </View>
      <View style={styles.halfContainer}>
        <TouchableOpacity
          onPress={() => alert("Hello, world!")}
          style={styles.button}
        >
          <Text style={styles.textButton}>button</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center"
  },
  halfContainer: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center"
  },
  textTitle: {
    fontSize: 60
  },
  textButton: {
    fontSize: 40
  },
  button: {
    backgroundColor: "skyblue",
    padding: 20,
    borderRadius: 5
  }
});
