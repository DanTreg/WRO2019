const mongoose = require("mongoose")

const Place = {
   Color: Number,
   Position: Number
}



const Row = {
   firstPlace: Place,
   secondPlace: Place,
   thirdPlace: Place
}


const ballPlaceSchema = mongoose.Schema({
   date: Date,
   active: Boolean,
   _id: mongoose.Schema.Types.ObjectId,
   firstRow: Row,
   secondRow: Row,
   thirdRow: Row

})



module.exports = mongoose.model('BallPlace', ballPlaceSchema)
