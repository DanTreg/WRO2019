import React from "react"



class BlockChainBlock extends React.Component {
    render(){
        const Enum = {
            0: "Transportation contract",
            1: "Manufacturer contract",
            2: "R&D contract"
        }
        return(
            <tr>
                <td scope="row">{this.props.block.index}</td>
                <td>{Enum[this.props.block.contractType]}</td>
                <td className="hash">{this.props.block.hash}</td>
            </tr>
            // {
            //     (typeof (this.props.block.data) === "")
            // }
        )
    }
}
export default BlockChainBlock