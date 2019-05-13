const mongoose = require("mongoose")


const FactoryStatusModel = mongoose.Schema({
    FactoryID: Number,
    _id: mongoose.Schema.Types.ObjectId,
    FactoryStatus: Number,
    date : Date
})


module.exports = mongoose.model('FactoryStatusModel', FactoryStatusModel)