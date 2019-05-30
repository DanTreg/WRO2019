import React, { Component } from 'react';
import Research from "./Research.js"
import TransportSystem from "./TransportSystem.js"
import BlockChain from "./BlockChain.js"
class Top extends Component{
    render(){
        return (
        <div className = "top-body">
            <Research />
            
            <TransportSystem />
            <BlockChain/>
        </div>
        )
    }
}

export default Top