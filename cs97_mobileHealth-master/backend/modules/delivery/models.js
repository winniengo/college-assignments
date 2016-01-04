/*
 * TSB - Delivery/Models.JS file
 * Defines the TSB Backend's database models for delivery aspects
 */

var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var orderLifecycleSchema = mongoose.Schema({
    order_number : String, 
    
    requester : String, //uuid of the requesting device
    deliverer : String, //uuid of the deliverer

    // status fields
    order_received : Boolean,
    order_accepted : Boolean,
    order_delivered : Boolean,
    order_failed : Boolean,

    // timestamp fields
    date_requested : Date,
    date_accepted: Date,
    date_delivered: Date,

    delivery_estimate : Number, 

    // specifics
    delivery_destination : { 
	dorm_name : String,
	dorm_room : Number, 
	delivery_type : String, 
	coordinates : 
        {lat: Number, lng: Number} //field for geo location
	},
    
    
    comments : [ {body: String, date: Date} ]

});


// export the different schemas as models
module.exports = {
    Order : mongoose.model('orderLifecycle', orderLifecycleSchema)
};