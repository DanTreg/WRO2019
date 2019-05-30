var express = require("express");
var router = express.Router();
var _ = require("lodash")
const mongoose = require("mongoose")
const filename = '../models/BlockChainBlockModel'
const BlockChainBlockModel = require(filename)
const tools = require("./tools.js")
const sha256 = require("sha256")
router.post("/", function(req, res){
    BlockChainBlockModel.find()
    .exec()
    .then(docs =>{

        var sorted = _.sortBy(docs, "index").reverse()
        var lastBlock = sorted[0]
        var lastIndex = lastBlock.index
        var newIndex = lastIndex += 1 
        var prevHash = lastBlock.hash
        var DateNow = new Date();
        if (req.body.isManufContract == 1){
            tools.fetchGetBallForCars()
            .then(result => {
                dataReq = result
                const BlockChainBlock = new BlockChainBlockModel({
                    _id: new mongoose.Types.ObjectId(),
                    timeStamp: DateNow,
                    prevHash: prevHash,
                    contractType: req.body.isManufContract,
                    index: newIndex,
                    data: dataReq,
                    hash: sha256(DateNow + newIndex + prevHash + dataReq)
                })
                BlockChainBlock.save().then(result1 => {
                    console.log(result1)
                    res.sendStatus(200)

                })
            })
      
        }
        else {
            dataReq = req.body.transpContract
            const BlockChainBlock = new BlockChainBlockModel({
                _id: new mongoose.Types.ObjectId(),
                timeStamp: DateNow,
                prevHash: prevHash,
                contractType: req.body.isManufContract,
                index: newIndex,
                data: dataReq,
                hash: sha256(DateNow + newIndex + prevHash + dataReq)
            })
            BlockChainBlock.save().then(result1 => {
                console.log(result1)
                res.sendStatus(200)
            })
        }


    
    })
})

router.get('/', function(req,res){
    BlockChainBlockModel.find()
    .exec()
    .then(docs => {
        res.json(docs)
    })
})
module.exports = router