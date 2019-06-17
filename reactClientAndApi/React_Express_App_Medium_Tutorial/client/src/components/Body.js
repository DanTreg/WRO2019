import React, { Component } from 'react';

import Top from "./Top.js"
import {IntlProvider} from 'react-intl';

class Body extends Component{
    render(){
        return (
        <IntlProvider locale="en">
          <div>
            <Top /> 
          </div>
        </IntlProvider>
        );
    }
}

export default Body