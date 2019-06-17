import React, {Component} from "react"
import * as CallApi from "../CallApi.js"
import { ButtonGroup, Button, CustomInput, Form, FormGroup, Spinner, Modal, ModalHeader, ModalBody, ModalFooter } from "reactstrap"
import BallsPlaces from "./BallsPlaces"
class Research extends Component{
    constructor(){
        super()
        this.state = {
            colorsToSubmit:{
                Red: false,
                White: false,
                Blue: false,
                Yellow:false,
                Green:false
            },
            modal: false,
            isLoadindg: false,
            BallsModel: []
        }
        this.fetchApi = this.fetchApi.bind(this)
        this.toggle = this.toggle.bind(this);
        this.handleChange = this.handleChange.bind(this)
        this.handleSubmit = this.handleSubmit.bind(this)
    }
    
    fetchApi(){
        this.setState(prevState =>({
            colorsToSubmit: prevState.colorsToSubmit,
            modal: prevState.modal,
            BallsModel: prevState.BallsModel,
            isLoadindg:true,
        }))
        console.log("we are in fetch api")
        CallApi.getAllBp().then((result)=>{
            console.log(result)
            this.setState(prevState =>({
                colorsToSubmit: prevState.colorsToSubmit,
                modal:prevState.modal,
                BallsModel:result,
                isLoadindg: !prevState.isLoadindg,
            }))
        })
        

        console.log(this.state.BallsModel)
    }
    componentDidMount(){
        this.fetchApi()
    }

    handleSubmit(){
        CallApi.createNewBp(this.state.colorsToSubmit)
        this.setState(prevState =>({
            colorsToSubmit:{
                Red: false,
                White: false,
                Blue: false,
                Yellow:false,
                Green:false
            },
            modal:prevState.modal,
            BallsModel:prevState.BallsModel,
            isLoadindg: prevState.isLoadindg,
        }))
        CallApi.postNewBlockchainBlock(2)
        this.toggle()
        setTimeout(this.fetchApi, 1000)
        
    }

    toggle() {
        this.setState(prevState => ({
            colorsToSubmit: prevState.colorsToSubmit,
            BallsModel: prevState.BallsModel,
            isLoadindg:prevState.isLoadindg,
            modal: !prevState.modal
        }))};
    
    handleChange(event){
        const { target } = event;
        const value = target.type === 'checkbox' ? target.checked : target.value;
        const { name } = target;
        // this.state.keys(this.state.colorsToSubmit).map(i => {
        //     if (i === name){
        //         this.setState(prevState({
        //             colorsToSubmit:{
        //                 [name]:value,

        //             }
        //         }))
        //     }
        // })
        var temp = this.state.colorsToSubmit
        temp[name] = value
        this.setState(prevState => ({
            colorsToSubmit:temp,
            BallsModel: prevState.BallsModel,
            isLoadindg:prevState.isLoadindg,
            modal:prevState.modal
        }))
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
                    <ButtonGroup className="SettingsResearch">
                        <Button color="success" onClick={this.fetchApi}>Update</Button>
                        <Button color="success" onClick={this.toggle}>Create New Product</Button>
                    </ButtonGroup>
                    {
                        this.state.BallsModel.map((object, i) => {
                            if (i === 0){
                                return(
                                    [<h2 style={{margin: "10%", marginTop:0, marginBottom:0}}>Market targeted product</h2>,
                                    <BallsPlaces colors = {object.temp} active = {true}/>,
                                    <hr/>,
                                    <h3 style={{margin: "10%", marginTop:0, marginBottom:0}}>History of development</h3>
                                    ])
                            }
                            else{
                                return(<BallsPlaces colors={object.temp} active={false} />)
                            }
                            
                        })
                        
                    }
                    <Modal isOpen={this.state.modal} toggle={this.toggle}>
                        <Form >
                            <ModalHeader >Create new product</ModalHeader>
                            <ModalBody>
                                
                                <FormGroup>
                                    <div>
                                        <CustomInput type="switch" id="RedColorSwitch" name="Red" onChange= {(e) => {
                                            this.handleChange(e)
                                        }} label={<span style={{backgroundColor : "red"}} class="circle"></span>}  />
                                        
                                        <CustomInput type="switch" id="BlueColorSwitch" name="Blue" onChange= {(e) => {
                                            this.handleChange(e)
                                        }} label={<span style={{backgroundColor : "blue"}} class="circle"></span>} />
                                        <CustomInput type="switch" id="YellowColorSwitch" name="Yellow" onChange= {(e) => {
                                            this.handleChange(e)
                                        }} label={<span style={{backgroundColor : "yellow"}} class="circle"></span>} />
                                        <CustomInput type="switch" id="GreenColorSwitch" name="Green" onChange= {(e) => {
                                            this.handleChange(e)
                                        }} label={<span style={{backgroundColor : "green"}} class="circle"></span>} />
                                        <CustomInput type="switch" id="WhiteColorSwitch" name="White" onChange= {(e) => {
                                            this.handleChange(e)
                                        }} label={<span style={{backgroundColor : "grey"}} class="circle"></span>} />
                                        <CustomInput type="switch" id="PurpleColorSwitch" name="Purple" label={<span style={{backgroundColor : "purple"}} class="circle"></span>} disabled />
                                        <CustomInput type="switch" id="BlackeColorSwitch" name="Black" label={<span style={{backgroundColor : "black"}} class="circle"></span>} disabled />
                                    </div>
                                </FormGroup>
                                
                            </ModalBody>
                            <ModalFooter>
                                <Button color="success" outline onClick={this.handleSubmit}>Submit</Button>
                            </ModalFooter>
                        </Form>
                    </Modal>
                </div>
            )
        }
        
    }

}
export default Research 