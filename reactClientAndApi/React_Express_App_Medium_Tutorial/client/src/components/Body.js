import React, { Component } from 'react';

import Top from "./Top.js"
import Bottom from "./Bottom.js"

class Body extends Component{
    render(){
        return (
        <div>
          <Top />
          <Bottom />  
        </div>
        );
    }
}

export default Body