var express = require("express");
var router = express.Router();
var _ = require("lodash")
const filename = '../models/BallsPlaceModel'
const BallsPlaceModel = require(filename)
const mongoose = require("mongoose")
const tools = require("./tools.js")




router.post("/",  function(req, res){

    console.log(req.body)


    var DateNow = new Date();

    const BallsPlace = new BallsPlaceModel({
        _id: new mongoose.Types.ObjectId(),
        date : DateNow,
        active: false,
        firstRow:{firstPlace:{Color:0,Position:0},secondPlace:{Color:0,Position:1},thirdPlace:{Color:0,Position:2}},
        secondRow:{firstPlace:{Color:0,Position:3},secondPlace:{Color:0,Position:4},thirdPlace:{Color:0,Position:5}},
        thirdRow:{firstPlace:{Color:0,Position:6},secondPlace:{Color:0,Position:7},thirdPlace:{Color:0,Position:8}}
    }
    )
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
        tools.activeAllFalse(sorted)
        tools.makeAllFalse()
        tools.replaceActive(activeModel)
        var finalModel = tools.convertModel(activeModel)
        res.json(finalModel).send()
    })
});

module.exports = router;
