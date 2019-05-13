var express = require("express");
var router = express.Router();
var _ = require("lodash")
const tools = require("./tools.js")
const filename = '../models/FactoryStatusModel'
const FactoryStatusModel = require(filename)




router.post("/", function (req, res) {
    var indexToChange
    FactoryStatusModel.find()

        .exec()
        .then(docs => {
            if (docs.length === 0) {
                tools.createNewFactoryStatusModel(req.body)
                res.status(200).send()
            }
            else {
                docs.forEach(element => {
                    if (element.FactoryID === req.body.FactoryID) {
                        indexToChange = docs.indexOf(element)
                    }
                });
                var test = typeof docs[indexToChange]
                if (test !== "undefined") {
                    if (docs[indexToChange].FactoryID === req.body.FactoryID) {
                        tools.replaceStatus(docs[indexToChange], req.body, "FactoryStatus")
                        res.status(200).send()
                    }
                    else {
                        tools.createNewFactoryStatusModel(req.body)
                        res.status(200).send()
                    }
                }
                else {
                    tools.createNewFactoryStatusModel(req.body)
                    res.status(200).send()
                }
            }

        })
    })

router.get("/", function (req, res, next) {
    FactoryStatusModel.find()
        .exec()
        .then(docs => {
            res.json(docs)
        })
})


module.exports = router;