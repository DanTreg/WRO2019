import React, {Component} from "react"
import * as CallApi from "../CallApi.js"
import { Spinner } from "reactstrap"
import BallsPlaces from "./BallsPlaces"
class Research extends Component{
    constructor(){
        super()
        this.state = {
            isLoadindg: false,
            BallsModel: []
        }
    }
    componentDidMount(){
        this.setState({
            isLoadindg:true
        })
        CallApi.getAllBp().then((result)=>{
            console.log(result)
            this.setState({
                BallsModel:result,
                isLoadindg:false
            })
        })
        

        console.log(this.state.BallsModel)
    }
    render(){
        if(this.state.isLoadindg === true){
            return(
                <div className= "ResearchDiv">
                    <Spinner color = "secondary"/>
                    <h3>Content is currently loading...</h3>
                </div>
            )
        }
        else{
            return(
                <div className = "ResearchDiv">
                    {
                        this.state.BallsModel.map((object, i) => {
                            if (i === 0){
                                return(<BallsPlaces colors = {object.temp} active = "true"/>)
                            }
                            else{
                                return(<BallsPlaces colors={object.temp} active="false" />)
                            }
                            
                        })
                        
                    }
                </div>
            )
        }
        
    }

}
export default Research 