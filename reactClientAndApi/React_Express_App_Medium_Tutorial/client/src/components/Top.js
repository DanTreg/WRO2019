import React, { Component } from 'react';
import Research from "./Research.js"
import PriceField from "./PriceField"
import BlockChain from "./BlockChain.js"
class Top extends Component{
    render(){
        return (
        <div className = "top-body">
            <Research />
            
            <PriceField />
            <BlockChain/>
        </div>
        )
    }
}

export default Top