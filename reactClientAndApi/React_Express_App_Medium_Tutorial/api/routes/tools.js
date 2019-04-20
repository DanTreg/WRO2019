const filename = '../models/BallsPlaceModel'
const BallsPlaceModel = require(filename)
const ManufacterModel = require("../models/ManufacterModel")
const mongoose = require("mongoose")
const _ = require("lodash")
const Enums = require("../models/Enums.js")

function covertArrToModel(arr){
    var finalObjectToReturn = { 
        firstPlace: arr[0],
        secondPlace: 0,
        thirdPlace: arr[1],
        fourthPlace: 0,
        fifthPlace: arr[2],
        sixthPlace: 0,
        seventhPlace: arr[3],
        eightsPlace: 0,
        ninethPlace: arr[4] 
    }
    return finalObjectToReturn
}

function randomIntIncluded(min, max){
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

module.exports = {
    activeAllFalse: function(docs){

        
        docs.forEach(element => {
            if (element.active != false){
                element.active = false
            }
        return docs
        });

    },
    convertModelToRoadController:function(docs){
        const FinalArr = []
        for(k = 0; k < docs.length; k++ ){
            FinalArr.push
            ({
                manufacturerID:docs[k].ManufacturerID,
                yellow:docs[k].ManufacturerInfoModel.y,
                green:docs[k].ManufacturerInfoModel.g,
                red:docs[k].ManufacturerInfoModel.r,
                blue:docs[k].ManufacturerInfoModel.b,
                white:docs[k].ManufacturerInfoModel.w
            }) 
        }
        return FinalArr
            // 

    },
    randomIntIncluded: function(min, max){
        return Math.floor(Math.random() * (max - min + 1)) + min;
    },
    createNewManufacturerInfoModel: function(someObject){
        var ManufacturerPayload = {
            r:someObject.balls.r,
            w:someObject.balls.w,
            y:someObject.balls.y,
            g:someObject.balls.g,
            b:someObject.balls.b
        }
        const ManufacturerInfo = new ManufacterModel({
            ManufacturerID: someObject.manufacturerID,
            _id: new mongoose.Types.ObjectId(),
            ManufacturerInfoModel: ManufacturerPayload

        })
        ManufacturerInfo.save().then(result =>{
            console.log(result)
        })

    },
    randomiseTemp: function(valArr){

        //TODO: Add algoritms for other colors,
        //optimize all of the process



        var neededAmount = 5
        var amountCollors
        var i
        var productModelArr = [0,0,0,0,0]


        //if (neededAmount === amountCollors){
        for(i = 0; i < productModelArr.length; i++){
            amountCollors = valArr.length //[r,g,b]
            
            randomAmount = randomIntIncluded(1, neededAmount - (amountCollors-1)) //random amount of balls for next color
            if (amountCollors === 1){
                randomAmount = 0;
                productModelArr.forEach(item => {
                    if (item === 0){
                        randomAmount++
                    }
                })
            }
            var amountOfItem = randomAmount //random amount of balls for next color
            var indexItem = valArr[Math.floor(Math.random()*valArr.length)] //random color
            var index = valArr.indexOf(indexItem); //index of chosen color
            neededAmount -= randomAmount
            
            for(j = 0; j < amountOfItem; j++ ){
                
                
                if (index > -1) {
                    var l = productModelArr.length
                    var temp = []
                    for (k=0;k<l;k++){
                        if( productModelArr[k]===0){
                            temp.push(k)
                        }
                    }
                    productModelArrIndex = temp[Math.floor(Math.random()*temp.length)]
                    productModelArr[productModelArrIndex] = Enums[indexItem]

                    }   
                }
                valArr.splice(index, 1);
            }
                
        return covertArrToModel(productModelArr)        
        },   
            
        //}
        //for(i = 0; i <= amountCollors; i++){ 
        //    var firstItem = valArr[Math.floor(Math.random()*valArr.length)];
        //    var amountOfFirstItem = randomIntIncluded(1, neededAmount - amountCollors)
        //}

    leaveOnlyVallible: function(object){
        var arr = []
        _.mapValues(object, (value, key, object) => {
            
            if (value === true){
                
                arr.push(key) 
            }
        });
        return arr
    },
    replaceInfoManufacturer: function (objectToUpdate, whatToReplace, Data){
        ManufacterModel.findById(objectToUpdate.id)
        .exec()
        .then(doc => {
            if(whatToReplace === "Data"){
                doc.ManufacturerInfoModel = {
                    r:Data.balls.r,
                    w:Data.balls.w,
                    y:Data.balls.y,
                    g:Data.balls.g,
                    b:Data.balls.b
                }
                doc.save()
            }
            return
            })

        },
        replaceInfo: function (objectToUpdate, whatToReplace, Data){
            BallsPlaceModel.findById(objectToUpdate.id)
            .exec()
            .then(doc => {
                if (whatToReplace === "Active"){
                    if (doc.active != true){
                        doc.active = true
    
                        }
                     doc.save()
                    }
                return
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
            "Color":object.temp.firstPlace
        },
        {  
            "Place":1,
            "Color":object.temp.secondPlace
        },
        {  
            "Place":2,
            "Color":object.temp.thirdPlace
        }
        ],
        [  
        {  
            "Place":3,
            "Color":object.temp.fourthPlace
        },
        {  
            "Place":4,
            "Color":object.temp.fifthPlace
        },
        {  
            "Place":5,
            "Color":object.temp.sixthPlace
        }
        ],
        [  
        {  
            "Place":6,
            "Color":object.temp.seventhPlace
        },
        {  
            "Place":7,
            "Color":object.temp.eightsPlace
        },
        {  
            "Place":8,
            "Color":object.temp.ninethPlace
        }
        ]
    ]
    return(finalModel)
    },
    updateCurrentDoc: function(docs){

    }
}