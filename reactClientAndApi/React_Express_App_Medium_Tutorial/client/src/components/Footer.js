import React, { Component } from 'react';
import { Container, Row, Col } from 'reactstrap';

class Footer extends Component{
    render(){
        return(
            <Container fluid={true} className="footer">
            <Row>
                <Col><h3>this is footer</h3></Col>
            </Row>
            </Container>
        )
    }
}

export default Footer