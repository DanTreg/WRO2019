import React, { Component } from 'react';
import * as CallApi from "../CallApi.js"
import {Spinner, Container, Row, Col} from "reactstrap"
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import CanvasJSReact from '../canvasjs.react';
var CanvasJS = CanvasJSReact.CanvasJS;
var CanvasJSChart = CanvasJSReact.CanvasJSChart;
class TransportSystem extends Component{
    constructor(){
        super()
        this.state = {
            CarStatus: [],
            isLoading:false
        }
        this.fetchAPI = this.fetchAPI.bind(this)
    }
    fetchAPI(){
        this.setState(prevState => ({
            isLoading:!prevState.isLoading,
            CarStatus:prevState.CarStatus
        }))
        CallApi.getAllBpCarStatus().then(result =>{
            this.setState(prevState =>({
                CarStatus:result,
                isLoading:!prevState.isLoading
            }))
        })
        console.log(this.state.CarStatus)
    }
    componentDidMount(){
        this.fetchAPI()
    }
    render(){
        if(this.state.isLoading === true){
            return(
                <div className= "TransportSystem">
                    <Spinner color = "secondary"/>
                    <h3>Content is currently loading...</h3>
                </div>
            )
        }
        return (
        <div className="TransportSystem">
                {   
                    this.state.CarStatus.map((object, i) =>{
                        const options = {
                            animationEnabled: true,
                            width: 200,
                            height:200,
                            theme: "light1", // "light1", "dark1", "dark2"
                            title:{
                                text: "Active and not active time"
                            },
                            data: [{
                                type: "pie",
                                indexLabel: "{label}: {y}%",		
                                startAngle: -90,
                                dataPoints: [
                                    { y: 20, label: "Active" },
                                    { y: 24, label: "Not active" },	
                                ]
                            }]
                        }
                        return(
                            <Container>
                                <Row>
                                    <Col>
                                        <h3 style={{marginTop:"1%"}}>Truck number:{object.CarID}</h3>
                                    </Col>
                                </Row>
                                <Row>
                                    <Col>
                                        <FontAwesomeIcon className="TransportIcons" icon= {"shipping-fast"} size="7x" color="#28a745" />
                                    </Col>
                                    <Col>
                                        <CanvasJSChart options = {options} />
                                    </Col>
                                </Row>

                            </Container>
                            // <div>
                            // <div className="Cars">
                                
                            //         <div style={{textAlign:"left"}}>
                            //             
                                        
                            //         </div>
                                        
                                    

                                    
                            //         <FontAwesomeIcon className="TransportIcons" icon= {"shipping-fast"} size="7x" color="#28a745" />
                            //     <hr/>
                            // </div>
                            //     <div >
                            //                     <CanvasJSChart options = {options} />
                            //     </div>
                            // </div>
                        )})
                }
            
            {/* <FontAwesomeIcon className="TransportIcons" icon= {"shipping-fast"} size="7x" color="#28a745" /><br/>
            <FontAwesomeIcon className="TransportIcons"icon= {"shipping-fast"} size="7x" color="#28a745" /> */}
        </div>

        )
    }
}

export default TransportSystem