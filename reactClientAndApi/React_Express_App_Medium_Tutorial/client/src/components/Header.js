import React, {Component} from "react"
import {
    Collapse,
    Navbar,
    NavbarToggler,
    NavbarBrand,
    Nav,
    NavItem,
    NavLink,Container, Row, Col
     } from 'reactstrap';

  
class Header extends Component{
    constructor(){
        super()
        this.toggleNavbar = this.toggleNavbar.bind(this);
        this.state = {
            collapsed: true
        };
    }
    
    toggleNavbar() {
        this.setState({
          collapsed: !this.state.collapsed
        });
      }
    
    render(){
        return(
            <Container fluid={true} className="header">
                <Row>
                    <Col>
                        <Navbar color="faded" light>
                            <NavbarBrand href="/" className="mr-auto">RoboMarket</NavbarBrand>
                            <NavbarToggler onClick={this.toggleNavbar} className="mr-2" />
                            <Collapse isOpen={!this.state.collapsed} navbar>
                                <Nav navbar>
                                    <NavItem>
                                        <NavLink href="https://github.com/DanTreg/WRO2019" target="_blank" >GitHub</NavLink>
                                    </NavItem>
                                </Nav>
                            </Collapse>
                        </Navbar>
                    </Col>
                </Row>
            </Container>
 
        )
    }
}

export default Header 