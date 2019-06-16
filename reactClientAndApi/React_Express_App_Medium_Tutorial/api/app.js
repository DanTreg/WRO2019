var createError = require("http-errors");
var express = require("express");
var path = require("path");
var cookieParser = require("cookie-parser");
var logger = require("morgan");
var cors = require("cors");



var indexRouter = require("./routes/index");
var usersRouter = require("./routes/users");
var testAPIRouter = require("./routes/testAPI");
var readJsonRouter = require("./routes/read_json");
var pushAvBallsRouter = require("./routes/pushAvaillable_balls")
var requestsForApiRouter = require("./routes/forApi.js")
var RoadStatusRouter = require("./routes/RoadStatus.js")
var FactoryStatusRouter = require("./routes/FactoryStatus.js")
var getBallForCarsRouter = require("./routes/getBallsForCars.js")
var CreateNewTransportationContract = require("./routes/CreateNewTransportationContract.js")
const mongoose = require("mongoose")

var app = express();

// view engine setup
app.set("views", path.join(__dirname, "views"));
app.set("view engine", "jade");
app.use(cors());
app.use(logger("dev"));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, "public")));



app.use("/", indexRouter);
app.use("/users", usersRouter);
app.use("/testAPI", testAPIRouter);
app.use("/BallPlacesApi", readJsonRouter);
app.use("/ManufacturerApi", pushAvBallsRouter);
app.use("/requestsForApi", requestsForApiRouter);
app.use("/RoadStatus", RoadStatusRouter);
app.use("/FactoryStatus", FactoryStatusRouter);
app.use("/getBallForCars", getBallForCarsRouter)
app.use("/createTranspContract", CreateNewTransportationContract)
// catch 404 and forward to error handler
app.use(function(req, res, next) {
    next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
    // set locals, only providing error in development
    res.locals.message = err.message;
    res.locals.error = req.app.get("env") === "development" ? err : {};

    // render the error page
    res.status(err.status || 500);
    res.render("error");
});



// replace the uri string with your connection string.
const uri = "mongodb://localhost:27017/SmartEconomics?retryWrites=true"
//const uri = "mongodb+srv://dbUser:admin@cluster0-lwiij.azure.mongodb.net/test?retryWrites=true"
mongoose.connect(uri,{ useNewUrlParser: true })
module.exports = app;
