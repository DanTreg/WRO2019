import React, {Component} from "react"
import * as CallApi from "../CallApi.js"
import { Spinner } from "reactstrap"
class Research extends Component{
    constructor(){
        super()
        this.state = {
            isLoadindg: false,
            BallsModel: {}
        }
    }
    componentDidMount(){
        CallApi.getAllBp().then((result)=>{
            console.log(result)
            this.setState({BallsModel:result})
        })
        

        console.log(this.state.BallsModel)
    }
    render(){
        if(this.state.isLoadindg === true){
            return(
                <div>
                    <Spinner color = "secondary"/>
                    <h1>Content is currently loading...</h1>
                </div>
            )
        }
        else{
            return(
                <div>
                    {JSON.stringify(this.state.BallsModel)}
                </div>
            )
        }
        
    }

}
export default Research 