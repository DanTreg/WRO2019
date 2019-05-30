const mongoose = require("mongoose")
const BlockChainBlock = mongoose.Schema({
    index : Number,
    timeStamp: Date,
    prevHash: String,
    _id: mongoose.Schema.Types.ObjectId,
    contractType: Number,
    data: Object,
    hash: String
})

module.exports = mongoose.model('BlockChainBlock', BlockChainBlock, 'blockchainblocks')