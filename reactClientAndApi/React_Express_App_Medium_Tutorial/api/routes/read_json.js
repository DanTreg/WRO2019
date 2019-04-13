var express = require("express");
var express = require("express");
var router = express.Router();
var _ = require("lodash")
const filename = '../models/BallsPlaceModel'
const BallsPlaceModel = require(filename)
const mongoose = require("mongoose")


router.put("/",  function(req, res){
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

function activeAllFalse(docs){

    
        docs.forEach(element => {
            if (element.active != false){
                element.active = false
            }
        return docs
        });

    }

function replaceActive(object){
    BallsPlaceModel.findById(object._id)
    .exec()
    .then(doc => {
        if (doc.active != true){
            doc.active = true
        
        }
        doc.save()
    })

}

function makeAllFalse(){
    BallsPlaceModel.update({"active":false})
}

function convertModel(object){
    var finalModel = 
    [  
        [  
           {  
              "Place":0,
              "Color":object.firstRow.firstPlace.Color
           },
           {  
              "Place":1,
              "Color":object.firstRow.secondPlace.Color
           },
           {  
              "Place":2,
              "Color":object.firstRow.thirdPlace.Color
           }
        ],
        [  
           {  
              "Place":3,
              "Color":object.secondRow.firstPlace.Color
           },
           {  
              "Place":4,
              "Color":object.secondRow.secondPlace.Color
           },
           {  
              "Place":5,
              "Color":object.secondRow.thirdPlace.Color
           }
        ],
        [  
           {  
              "Place":6,
              "Color":object.thirdRow.firstPlace.Color
           },
           {  
              "Place":7,
              "Color":object.thirdRow.secondPlace.Color
           },
           {  
              "Place":8,
              "Color":object.thirdRow.thirdPlace.Color
           }
        ]
     ]
     return(finalModel)
}

router.get("/",  function(req, res, next) {


    BallsPlaceModel.find()
    .exec()
    .then(docs => {
        var sorted = _.sortBy(docs, "date").reverse();
        var activeModel = sorted[0]
        activeAllFalse(sorted)
        makeAllFalse()
        replaceActive(activeModel)
        var finalModel = convertModel(activeModel)
        res.json(finalModel).send()
    })
});

module.exports = router;
