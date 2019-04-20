var express = require("express");
var router = express.Router();
var _ = require("lodash")
const filename = '../models/ManufacterModel'
const ManufacterModel = require(filename)
const mongoose = require("mongoose")
const tools = require("./tools.js")

router.post("/",  function(req, res){
    var indexToChange
    ManufacterModel.find()
    
    .exec()
    .then(docs => {
            if (docs.length === 0){
                tools.createNewManufacturerInfoModel(req.body)
            }
            else{
                docs.forEach(element => {
                    if(element.ManufacturerID === req.body.manufacturerID){
                        indexToChange = docs.indexOf(element)
                    }
                });
                var test = typeof docs[indexToChange]
                if (test !== "undefined"){    
                    if (docs[indexToChange].ManufacturerID === req.body.manufacturerID  ){
                        tools.replaceInfoManufacturer(docs[indexToChange], "Data", req.body)
                        res.status(200).send()
                    }
                    else{
                        tools.createNewManufacturerInfoModel(req.body)
                        res.status(200).send()
                    }}
                else{
                    tools.createNewManufacturerInfoModel(req.body)
                    res.status(200).send()
                }
        }
                
    })
})


router.get("/",  function(req, res, next) {
    ManufacterModel.find()
    
    .exec()
    .then(docs => {
       res.json(tools.convertModelToRoadController(docs) ).send()

    })
});
module.exports = router;