import React, {Component} from "react"
import * as CallApi from '../CallApi.js'
class Header extends Component{
    
    handleClick(){
        console.log("I was clicked")
        CallApi.createNewBp()
    }
    
    render(){
        return(
            <div className="header">
                <button onClick={this.handleClick} className="button-header">create new bp</button>
                <button className="button-header">About</button>
                <button className="button-header">Coontent</button>
            </div>
        )
    }
}

export default Header 