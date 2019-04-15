const filename = '../models/BallsPlaceModel'
const BallsPlaceModel = require(filename)
const mongoose = require("mongoose")

module.exports = {
    activeAllFalse: function(docs){

        
        docs.forEach(element => {
            if (element.active != false){
                element.active = false
            }
        return docs
        });

    },

    replaceActive: function (object){
        BallsPlaceModel.findById(object._id)
        .exec()
        .then(doc => {
            if (doc.active != true){
                doc.active = true

        }
            doc.save()
    })

    },

    makeAllFalse: function (){
        BallsPlaceModel.update({"active":false})
    }, 

    convertModel: function(object){
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
}