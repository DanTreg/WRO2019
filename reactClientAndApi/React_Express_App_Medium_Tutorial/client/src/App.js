import React, { Component } from 'react';
import './App.css';
import Header from "./components/Header.js"
import Footer from "./components/Footer.js"
import Body from "./components/Body.js"
import { library } from '@fortawesome/fontawesome-svg-core'
import { faShippingFast, faIndustry } from '@fortawesome/free-solid-svg-icons'
library.add(faShippingFast, faIndustry)
class App extends Component {

  render() {
    return(
      <div>
        <Header/>
        <Body />
        <Footer/>
      </div>
    )
  }
}

export default App;
