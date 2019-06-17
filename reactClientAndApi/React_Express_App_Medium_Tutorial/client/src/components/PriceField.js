import React, { Component } from 'react';
import * as CallApi from "../CallApi.js"

import CanvasJSReact from '../canvasjs.react';
import {FormattedNumber} from 'react-intl';

var CanvasJSChart = CanvasJSReact.CanvasJSChart;
class PriceField extends Component{
    constructor(){
        super()
        
        this.state = {
            marketValue: 0,
        }
        this.fetchAPI = this.fetchAPI.bind(this)
    }
    fetchAPI(){
        CallApi.getAllBp().then(result =>{
            var marketValueResult = result[0].marketValue
            this.setState({
                marketValue: marketValueResult
            })
        })
    }
    componentDidMount(){
        this.fetchAPI()
        setInterval(this.fetchAPI, 1000)
    }
    render(){
        const options = {
            animationEnabled: true,
            width: 600,
            height: 400,
            theme: "light1", // "light1", "dark1", "dark2"
            title: {
                text: "Division of the market"
            },
            data: [{
                type: "pie",
                indexLabel: "{label}: {y}%",
                startAngle: -90,
                dataPoints: [{
                        y: 25,
                        label: "Suppliers of components"
                    },
                    {
                        y: 12.5,
                        label: "Research and development"
                    },
                    {
                        y: 12.5,
                        label: "Utillities"
                    },
                    {
                        y: 50,
                        label: "Investors"
                    },
                ]
            }]
        }
        return(
            
            <div className = "TransportSystem">

                <h3>Market value: <FormattedNumber value={this.state.marketValue} style="currency" currency="USD"/></h3>
                <CanvasJSChart options = {options} />
                    <table>
                        <tr>
                            <td>
                                 <h3> Investors part:</h3>

                            </td>
                            <td>
                                <h3><FormattedNumber value={this.state.marketValue * 0.50} style="currency" currency="USD"/></h3>
                            </td>
                        </tr>
                        <tr>
                            <td><h3>Utillities part:</h3></td>
                            <td><h3><FormattedNumber value={this.state.marketValue * 0.125} style="currency" currency="USD"/></h3></td>
                        </tr>
                        <tr>
                            <td><h3>Research and development:</h3></td>
                            <td><h3><FormattedNumber value={this.state.marketValue * 0.125} style="currency" currency="USD"/></h3></td>
                        </tr>
                        <tr>
                            <td><h3>Suppliers of components:</h3></td>
                            <td><h3><FormattedNumber value={this.state.marketValue * 0.25} style="currency" currency="USD"/></h3></td>
                        </tr>
                        <tr>
                            <td><h3>Including Taxes, 10%</h3></td>
                            <td><h3><FormattedNumber value={this.state.marketValue * 0.1} style="currency" currency="USD"/></h3></td>
                        </tr>
                    </table>
            </div>
        )
    }
}

export default PriceField