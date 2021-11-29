import React from 'react';
import {shallow} from 'enzyme';
import Submissions from '../Submissions';
import renderer from 'react-test-renderer';
import theme from '../../../../Theme/Dark';
import {ThemeProvider} from '@material-ui/core/styles';
import {MuiThemeProvider} from '@material-ui/core';
import StandardLayout from '../../../../Components/Layouts/StandardLayout';


describe('Basic and Shallow Mount Test Submissions Component', () => {
  it('Basic Render Submissions Component', ()=>{
    const wrapper = renderer.create(
      <ThemeProvider theme={theme}>
        <Submissions/>
      </ThemeProvider>).toJSON();
    expect(wrapper).toMatchSnapshot();
  });
  it('Shallow render Submissions Component', () => {
    const wrapper = shallow(<Submissions/>);
    expect(wrapper).toMatchSnapshot();
  });
});
