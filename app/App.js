import React from 'react';
import { useFonts } from '@use-expo/font';
import { AppLoading } from 'expo';
import { View } from 'react-native';
import DropdownAlert from 'react-native-dropdownalert';

import Home from './Home';
import DropDownHolder from './DropDownHolder';

export default () => {
  const [fontsLoaded] = useFonts({
    'Agency FB': require('./assets/fonts/agency-fb.ttf'),
  });

  if (!fontsLoaded) {
    return <AppLoading />;
  }
  return (
    <View style={{ width: '100%', height: '100%' }}>
      <Home />
      <DropdownAlert ref={(ref) => DropDownHolder.setDropDown(ref)} />
    </View>
  );
};
