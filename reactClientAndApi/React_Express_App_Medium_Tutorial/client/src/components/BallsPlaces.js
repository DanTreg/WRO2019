import React from "react"
import { Table } from 'reactstrap'
import Enum from "../Enum.js"
class BallsPlaces extends React.Component{
    constructor(){
        super()
        this.state={
            TableType:""
        }
    }
    componentDidMount(){
        if(this.props.active === true){
            this.setState({
                TableType: "active"
            })
        }
        else{
            this.setState({
                TableType: "innactive"
            })
        }
    }
    render(){
        return(
        <Table className={"table-balls-" + this.state.TableType }  responsive bordered>
            <tr>
                <td className="BallsTableTd">
                    <span style={{backgroundColor : Enum[this.props.colors.firstPlace]}} class="circle"></span>
                </td>
                <td className="BallsTableTd">
                    <span style={{backgroundColor : Enum[this.props.colors.secondPlace]}} class="circle"></span>
                </td>
                <td className="BallsTableTd">
                    <span style={{backgroundColor : Enum[this.props.colors.thirdPlace]}} class="circle"></span>
                </td>
                
            </tr>
            <tr>
                <td className="BallsTableTd">
                    <span style={{backgroundColor : Enum[this.props.colors.fourthPlace]}} class="circle"></span>
                </td>
                <td className="BallsTableTd">
                    <span style={{backgroundColor : Enum[this.props.colors.fifthPlace]}} class="circle"></span>
                </td>
                <td className="BallsTableTd">
                    <span style={{backgroundColor : Enum[this.props.colors.sixthPlace]}} className="circle"></span>
                </td>
                
            </tr>
            <tr>
                <td className="BallsTableTd">
                    <span style={{backgroundColor : Enum[this.props.colors.seventhPlace]}}  class="circle"></span>
                </td>
                <td className="BallsTableTd">
                    <span style={{backgroundColor : Enum[this.props.colors.eightsPlace]}} class="circle"></span>
                </td>
                <td className="BallsTableTd">
                    <span style={{backgroundColor : Enum[this.props.colors.ninethPlace]}} class="circle"></span>
                </td>
                
            </tr>

            
        </Table>)
    }
}
export default BallsPlaces