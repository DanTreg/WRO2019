import React, {Component} from "react"
import * as CallApi from '../CallApi.js'
import { Button } from 'reactstrap'
class Header extends Component{
    
    handleClick(){
        console.log("I was clicked")
        CallApi.createNewBp()
    }
    
    render(){
        return(
            <div className="header">
                <Button color="secondary" onClick={this.handleClick} className="button-header">create new bp</Button>
                <Button className="button-header">About</Button>
                <Button className="button-header">Coontent</Button>
            </div>
        )
    }
}

export default Header 