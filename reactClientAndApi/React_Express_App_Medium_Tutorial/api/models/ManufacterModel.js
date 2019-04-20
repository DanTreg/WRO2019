const mongoose = require("mongoose")


const ManufacterInfoModel = {
        r: Number,
        w: Number,
        y: Number,
        g: Number,
        b: Number
}

const ManufacterInfo = mongoose.Schema({
    ManufacturerID:Number,
    _id: mongoose.Schema.Types.ObjectId,
    ManufacturerInfoModel: ManufacterInfoModel
 })


module.exports = mongoose.model('ManufacterInfo', ManufacterInfo)
