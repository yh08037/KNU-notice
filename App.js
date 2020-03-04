import React, { useState, Component } from "react";
import { StyleSheet, Text, View, StatusBar, Switch } from "react-native";

export default class App extends Component {
  state = {
    isNoticeOn: true,
    isCoronaOn: true
  };

  _toggleNotice = () =>
    this.setState(state => ({
      isNoticeOn: !state.isNoticeOn
    }));

  _toggleCorona = () =>
    this.setState(state => ({
      isCoronaOn: !state.isCoronaOn
    }));

  render() {
    console.log(this.state.switchValue);
    return (
      <View style={styles.container}>
        <StatusBar barStyle="dark-content" />
        <View style={styles.halfContainer}>
          <Text style={styles.textTitle}>KNU Notice</Text>
        </View>
        <View style={styles.halfContainer}>
          <View style={styles.elem}>
            <Text style={styles.textSwitch}>경북대학교 공지사항</Text>
            <Switch
              style={styles.switch}
              onValueChange={this._toggleNotice}
              value={this.state.switchValue}
              trackColor="orange"
            />
          </View>
          <View style={styles.elem}>
            <Text style={styles.textSwitch}>코로나19 대응 관련 공지</Text>
            <Switch
              style={styles.switch}
              onValueChange={this._toggleCorona}
              value={this.state.switchValue}
              trackColor="orange"
            />
          </View>
        </View>
      </View>
    );
  }
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

  elem: {
    width: "100%",
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-around",
    borderColor: "#eee",
    borderBottomWidth: 0.5,
    paddingLeft: 5
  },
  textSwitch: {
    fontSize: 16,
    flexDirection: "row",
    alignItems: "center"
  },
  switch: {
    padding: 8,
    paddingLeft: 5
  }
});
