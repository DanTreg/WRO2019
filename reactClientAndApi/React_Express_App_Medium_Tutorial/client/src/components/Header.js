import React, {Component} from "react"
import * as CallApi from '../CallApi.js'
import {
    ButtonGroup,
    Button,
    Collapse,
    Navbar,
    NavbarToggler,
    NavbarBrand,
    Nav,
    NavItem,
    NavLink,
    UncontrolledDropdown,
    DropdownToggle,
    DropdownMenu,
    DropdownItem } from 'reactstrap';
  
class Header extends Component{
    constructor(){
        super()
        this.state = {
            isOpen: false
        };
    }
    handleClick(){
        console.log("I was clicked")
        CallApi.createNewBp()
    }
    toggleNavbar() {
        this.setState({
          collapsed: !this.state.collapsed
        });
      }
    
    render(){
        return(
            <div className="header">
                {/* 
                <Button className="button-header">About</Button>
                <Button className="button-header">Coontent</Button> */}
                <Navbar color="#ffffff" light expand="md">
                    <NavbarBrand href="/">RoboMarket</NavbarBrand>
                    <NavbarToggler onClick={this.toggle} />
                    <Collapse isOpen={this.state.isOpen} navbar>
                        <Nav tabs className="ml-auto" navbar>
                            <ButtonGroup>
                                <NavItem>
                                    <Button onClick={this.handleClick}>CreatenewBP</Button>
                                </NavItem>

                                <UncontrolledDropdown outline >
                                    <DropdownToggle caret >
                                        Options
                                    </DropdownToggle>
                                    <DropdownMenu right>
                                        <DropdownItem>
                                            Option 1
                                        </DropdownItem>
                                        <DropdownItem>
                                            Option 2
                                        </DropdownItem>
                                        <DropdownItem divider />
                                        <DropdownItem>
                                            Reset
                                        </DropdownItem>
                                    </DropdownMenu>
                                </UncontrolledDropdown>
                            </ButtonGroup>
                        </Nav>
                    </Collapse>
                </Navbar>
            </div>
        )
    }
}

export default Header 