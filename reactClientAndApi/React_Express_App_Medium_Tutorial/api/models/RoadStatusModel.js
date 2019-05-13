const mongoose = require("mongoose")


const RoadStatusModel = mongoose.Schema({
    CarID:Number,
    _id: mongoose.Schema.Types.ObjectId,
    CarStatus: Number,
    date: Date
 })

 
module.exports = mongoose.model('RoadStatusModel', RoadStatusModel)