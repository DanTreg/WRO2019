import React, { Component } from 'react';
import Research from "./Research.js"
import TransportSystem from "./TransportSystem.js"
import FactoryStatus from "./FactoryStatus.js"
import { Container, Row, Col } from 'reactstrap';
class Top extends Component{
    render(){
        return (
        <Container fluid={true} className = "top-body">
            <Row>
            <Col>
                <Research />
            </Col>
            <Col>
                <TransportSystem />
            </Col>
            <Col>
                <FactoryStatus/>
            </Col>
            </Row>
        </Container>
        )
    }
}

export default Top