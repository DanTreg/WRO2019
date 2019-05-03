import React, { Component } from 'react';
import Research from "./Research.js"
import TransportSystem from "./TransportSystem.js"
import FactoryStatus from "./FactoryStatus.js"
class Top extends Component{
    render(){
        return (
        <div className = "top-body">
            <Research />
            
            <TransportSystem />
            <FactoryStatus/>
        </div>
        )
    }
}

export default Top