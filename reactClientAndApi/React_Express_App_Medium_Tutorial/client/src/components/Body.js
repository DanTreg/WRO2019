import React, { Component } from 'react';
import { Container, Row, Col } from 'reactstrap';
import Top from "./Top.js"
import Bottom from "./Bottom.js"

class Body extends Component{
    render(){
        return (
        <Container fluid={true} className="main-top">
          <Row>
            <Top />
          </Row>
          <hr/>
          <Row>
            <Bottom />
          </Row>
        </Container>
        );
    }
}

export default Body