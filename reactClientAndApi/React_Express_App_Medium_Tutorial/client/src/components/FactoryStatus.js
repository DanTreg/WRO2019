import React, { Component } from 'react';
import * as CallApi from "../CallApi.js"
import { Spinner, Container, Row, Col } from "reactstrap"
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import CanvasJSReact from '../canvasjs.react';
var CanvasJS = CanvasJSReact.CanvasJS;
var CanvasJSChart = CanvasJSReact.CanvasJSChart;
class FactoryStaus extends Component{
    constructor() {
        super()
        this.state = {
            FactoryStatus: [],
            isLoading: false
        }
        this.fetchAPI = this.fetchAPI.bind(this)
    }
    fetchAPI() {
        this.setState(prevState => ({
            isLoading: !prevState.isLoading,
            FactoryStatus: prevState.FactoryStatus
        }))
        CallApi.getAllBpFactoryStatus().then(result => {
            this.setState(prevState => ({
                FactoryStatus: result,
                isLoading: !prevState.isLoading
            }))
        })
        console.log(this.state.FactoryStatus)
    
    }
    componentDidMount() {
        this.fetchAPI()
    }
    render(){
        if(this.state.isLoading === true){
            return (
                <div className="FactoryStatus">
                    <Spinner color="secondary" />
                    <h3>Content is currently loading...</h3>
                </div>
            )
        }
        return (
        <div className="FactoryStatus">
            {
                    this.state.FactoryStatus.map((object, i) => {
                    const options = {
                        animationEnabled: true,
                        width: 200,
                        height: 200,
                        theme: "light1", // "light1", "dark1", "dark2"
                        title: {
                            text: "Active and not active time"
                        },
                        data: [{
                            type: "pie",
                            indexLabel: "{label}: {y}%",
                            startAngle: -90,
                            dataPoints: [
                                { y: 24, label: "Active" },
                                { y: 30, label: "Not active" },
                            ]
                        }]
                    }
                    return (
                        <Container>
                            <Row>
                                <Col>
                                    <h3 style={{ marginTop: "1%" }}>Factory number:{object.FactoryID}</h3>
                                </Col>
                            </Row>
                            <Row>
                                <Col>
                                    <FontAwesomeIcon className="TransportIcons" icon={"industry"} size="7x" color="#28a745" />
                                </Col>
                                <Col>
                                    <CanvasJSChart options={options} />
                                </Col>
                            </Row>

                        </Container>
                    )
                })
            }
        </div>
        )
    }
}

export default FactoryStaus