var express = require("express");
var router = express.Router();
var _ = require("lodash")
const filename = '../models/RoadStatusModel.js'
const RoadStatusModel = require(filename)
const mongoose = require("mongoose")
const tools = require("./tools.js")


router.post("/",  function(req, res){
    var indexToChange
    RoadStatusModel.find()
    
    .exec()
    .then(docs => {
            if (docs.length === 0){
                tools.createNewRoadStatusModel(req.body)
                res.status(200).send()
            }
            else{
                docs.forEach(element => {
                    if(element.CarID === req.body.CarID){
                        indexToChange = docs.indexOf(element)
                    }
                });
                var test = typeof docs[indexToChange]
                if (test !== "undefined"){    
                    if (docs[indexToChange].CarID === req.body.CarID  ){
                        tools.replaceStatus(docs[indexToChange], req.body, "RoadStatus")
                        res.status(200).send()
                    }
                    else{
                        tools.createNewRoadStatusModel(req.body)
                        res.status(200).send()
                    }}
                else{
                    tools.createNewRoadStatusModel(req.body)
                    res.status(200).send()
                }
        }
                
    })
})
router.get("/", function(req, res, next){
    RoadStatusModel.find()
        .exec()
        .then(docs =>{
            res.json(docs)
        })
})

module.exports = router;