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
   active: Boolean,
   _id: mongoose.Schema.Types.ObjectId,
   temp: modelTemp

})



module.exports = mongoose.model('BallPlace', ballPlaceSchema)
