import React, { Component } from 'react';
import './App.css';
import Header from "./components/Header.js"
import Footer from "./components/Footer.js"
import Body from "./components/Body.js"
class App extends Component {


      constructor() {
          super();
          this.state = {
               apiResponse: "",
               test:"fds" 
            };
      }

        componentWillMount() {
            //callAPI.getBP();
            //console.log(this.state.apiResponse)
        }

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
