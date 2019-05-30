import React from "react"
import { Table } from 'reactstrap'


class BlockChainBlock extends React.Component {
    render(){
        return(
            <tr>
                <td scope="row">{this.props.block.index}</td>
                <td>{(this.props.block.contractType == 0) ? "Transportation contract" : "Manufacturer contract"}</td>
                <td></td>
                <td className="hash">{this.props.block.hash}</td>
            </tr>
            // {
            //     (typeof (this.props.block.data) === "")
            // }
        )
    }
}
export default BlockChainBlock