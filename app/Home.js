import React from 'react';
import {
  View, Text, StyleSheet, TouchableOpacity, Keyboard
} from 'react-native';
import SmoothPinCodeInput from 'react-native-smooth-pincode-input';

import API from './API';
import DropDownHolder from './DropDownHolder';


class Home extends React.Component {
  constructor() {
    super();
    this.state = { roll_count: 6, pin_modal: false, pin: '' };
    this.pinInput = React.createRef();
  }

  async componentDidMount() {
    this.keyboardDidHideListener = Keyboard.addListener('keyboardDidHide', this.keyboardDidHide);
    let call = await API.get_status();
    if (call.success === true) {
      DropDownHolder.throwSuccess('Connected to TPaaS System');
      if (call.data.rolls_remaining >= 0) this.setState({ roll_count: call.data.rolls_remaining });
    }
  }

  componentWillUnmount() {
    this.keyboardDidHideListener.remove();
  }

  // Hide PIN modal when keyboard is no longer on screen
  keyboardDidHide = () => {
    this.setState({ pin_modal: false, pin: '' });
  }

  async check_pin(code) {
    let pin_check = await API.get_dispense(code);
    if (!pin_check.success) {
      colors.modal_bg = 'red';
      setTimeout(() => {
        colors.modal_bg = colors.primary;
        this.setState({ pin: '' });
      }, 1000);
      return false;
    }

    return true;
  }

  async dispense(pin) {
    let { roll_count } = this.state;
    if (roll_count < 1) {
      DropDownHolder.throwError('Out of Rolls. Please re-stock dispenser and try again.');
    }
    let call = await API.get_dispense(pin);
    if (!call.success) {
      // Condition for invalid auth
      if (call.reason && call.reason.toLowerCase().includes('authentication')) {
        DropDownHolder.throwError(call.reason);
        colors.modal_bg = 'red';
        setTimeout(() => {
          colors.modal_bg = colors.primary;
          this.setState({ pin: '' });
        }, 1000);
      } else {
        DropDownHolder.throwError(call.reason);
      }
      this.setState({ pin: '' });
      return;
    }
    DropDownHolder.throwSuccess('Authentication Successful! Enjoy!');
    this.setState({ roll_count: roll_count - 1 });
    this.setState({ pin_modal: false, pin: '' });
  }


  render_controls() {
    let { pin_modal, pin } = this.state;
    if (!pin_modal) {
      return (
        <TouchableOpacity
          style={styles.Button}
          onPress={() => {
            if (this.state.roll_count < 1) {
              DropDownHolder.throwError('Out of Rolls. Please re-stock dispenser and try again.');
            } else {
              API.get_generate_pin().then((result) => {
                if (!result.success) {
                  DropDownHolder.throwError(result.reason);
                }
                this.setState({ pin_modal: true });
              });
            }
          }}
        >
          <Text style={styles.ButtonText}>Dispense</Text>
        </TouchableOpacity>
      );
    }
    return (
      <View style={[styles.PinView, { backgroundColor: colors.modal_bg }]}>
        <Text style={{
          textAlign: 'center', fontFamily: font_family, color: colors.secondary, fontSize: 48, paddingBottom: 20
        }}
        >
          Enter PIN
        </Text>
        <SmoothPinCodeInput
          ref={this.pinInput}
          cellStyle={{
            borderBottomWidth: 2,
            borderColor: 'gray',
          }}
          cellStyleFocused={{
            borderColor: 'white',
          }}
          textStyle={{ fontFamily: font_family, fontSize: 48, color: colors.secondary }}
          autoFocus
          restrictToNumbers
          keyboardType="numeric"
          value={pin}
          onTextChange={(code) => this.setState({ pin: code })}
          onFulfill={(code) => this.dispense(code)}
          // onBlur={() => this.setState({ pin_modal: false })}
        />
      </View>
    );
  }

  render() {
    let { roll_count } = this.state;
    let control = this.render_controls();

    return (
      <View style={styles.Container}>
        <View style={{
          flex: 1, flexWrap: 'wrap', alignSelf: 'stretch', justifyContent: 'center', alignContent: 'center'
        }}
        >
          <Text style={[styles.Text, {
            fontSize: 212,
            textAlign: 'center',
          }]}
          >
            {roll_count}
          </Text>
          <Text
            numberOfLines={2}
            style={[styles.Text, {
              textAlign: 'center', textAlignVertical: 'center', width: 200
            }]}
          >
            Rolls Remaining
          </Text>

        </View>

        <View style={{ flex: 1, justifyContent: 'center' }}>
          {control}
        </View>
      </View>
    );
  }
}

const colors = {
  primary: '#161616',
  secondary: '#fefefe',
  background: '#91AAC9',
  modal_bg: '#161616'
};

const font_family = 'Agency FB';

const styles = StyleSheet.create({
  Container: {
    flex: 1,
    flexDirection: 'column',
    backgroundColor: colors.background,
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: '5%',
    paddingTop: 25
  },
  Text: {
    fontFamily: font_family,
    color: colors.primary,
    fontSize: 48
  },
  Button: {
    backgroundColor: colors.primary,
    borderRadius: 10,
    borderWidth: 1,
    paddingHorizontal: 40,
    paddingVertical: 10,
    // marginBottom: '10%'
  },
  ButtonText: {
    color: colors.secondary,
    fontFamily: font_family,
    fontSize: 64
  },
  PinView: {
    paddingHorizontal: 40,
    paddingVertical: 20,
    borderRadius: 10,
    borderWidth: 1,
  }
});


export default Home;
