var express = require("express");
var router = express.Router();
var _ = require("lodash")
const filename = '../models/BallsPlaceModel'
const BallsPlaceModel = require(filename)
const mongoose = require("mongoose")


router.get("/", function(req, res){
    BallsPlaceModel.find()
    .exec()
    .then(docs => {
        var sortedByDate= _.sortBy(docs, "date").reverse()
        res.json(sortedByDate)
    })
})

module.exports = router;
