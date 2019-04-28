var express = require("express");
var router = express.Router();
var _ = require("lodash")
const filename = '../models/BallsPlaceModel'
const BallsPlaceModel = require(filename)
const mongoose = require("mongoose")
const tools = require("./tools.js")




router.post("/",  function(req, res){

    console.log(req.body)
    
    var varArr = tools.leaveOnlyVallible(req.body)
    var DateNow = new Date();

    const BallsPlace = new BallsPlaceModel({
        _id: new mongoose.Types.ObjectId(),
        date : DateNow,
        temp: tools.randomiseTemp(varArr) 
    })
    BallsPlace.save().then(result =>{
        console.log(result)
    
    })
    res.status(200).send()
    

})

router.get("/",  function(req, res, next) {

    BallsPlaceModel.find()
    .exec()
    .then(docs => {
    var sorted = _.sortBy(docs, "date").reverse();
    var activeModel = sorted[0]
    var finalModel = tools.convertModel(activeModel)
    console.log(activeModel)
    res.json(finalModel).send()
    })
    
});

module.exports = router;
