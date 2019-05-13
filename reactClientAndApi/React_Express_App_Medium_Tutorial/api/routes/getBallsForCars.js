var express = require("express");
var router = express.Router();
var _ = require("lodash")
const tools = require("./tools.js")
const ManufacturerModel = require("../models/ManufacterModel")
const BallsPlaceModel = require("../models/BallsPlaceModel")



router.get("/", function (req, res, next) {
    ManufacturerModel.find()
        .exec()
        .then(ManufacturerModel => {
            tools.getActiveBallPlace()
            .then(result => {
                res.json(tools.countNeededBalls(ManufacturerModel, result))
            })
        })
})



module.exports = router;