import React, { Component } from 'react';
import * as CallApi from "../CallApi.js"
import { Spinner, Table } from "reactstrap"
import BlockChainBlock from "./BlockchainBlock"
class BlockChain extends Component{
    constructor() {
        super()
        this.state = {
            BlockChain: [],
            isLoading: false
        }
        this.fetchAPI = this.fetchAPI.bind(this)
    }
    fetchAPI() {
        this.setState(prevState => ({
            isLoading: !prevState.isLoading,
            BlockChain: prevState.FactoryStatus
        }))
        CallApi.getAllBlockChain().then(result => {
            this.setState(prevState => ({
                BlockChain: result,
                isLoading: !prevState.isLoading
            }))
        })
    
    }
    
    componentDidMount() {
        this.fetchAPI()
        setInterval(this.fetchAPI, 10000)
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
            <Table hover>
                <thead>
                    <tr>
                        <th>Block Number</th>
                        <th>Contract type</th>
                        <th>Hash</th>
                    </tr>
                </thead>
                <tbody>
                    {
                        this.state.BlockChain.map((obj) => {
                            return(
                                <BlockChainBlock block={obj}/>
                            )
                        })
                    }
                </tbody>
            </Table>
        </div>
        )
    }
}

export default BlockChain