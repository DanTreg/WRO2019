import React, { Component } from 'react';
import { Container, Row, Col } from 'reactstrap';
import './App.css';
import Header from "./components/Header.js"
import Footer from "./components/Footer.js"
import Body from "./components/Body.js"
import { library } from '@fortawesome/fontawesome-svg-core'
import { faShippingFast } from '@fortawesome/free-solid-svg-icons'
library.add(faShippingFast)
class App extends Component {

  render() {
    return(
        <Container fluid={true} className="Main-Container">
          <Container fluid={true}>
          <Row>
              <Header/>
          </Row>
          </Container>
          <Container fluid={true}>
          <Row>
            <Body />
          </Row>
          </Container>
          <Container fluid={true}>
          <Row>
            <Footer/>
          </Row>
          </Container>
        </Container>
    )
  }
}

export default App;
