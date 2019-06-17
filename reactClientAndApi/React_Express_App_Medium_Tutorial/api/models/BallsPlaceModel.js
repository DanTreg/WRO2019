const mongoose = require("mongoose")

const modelTemp = {
   firstPlace: Number,
   secondPlace: Number,
   thirdPlace: Number,
   fourthPlace: Number,
   fifthPlace: Number,
   sixthPlace: Number,
   seventhPlace: Number,
   eightsPlace: Number,
   ninethPlace: Number,


}

const ballPlaceSchema = mongoose.Schema({
   date: Date,
   _id: mongoose.Schema.Types.ObjectId,
   temp: modelTemp,
   marketValue: Number

})



module.exports = mongoose.model('BallPlace', ballPlaceSchema)
