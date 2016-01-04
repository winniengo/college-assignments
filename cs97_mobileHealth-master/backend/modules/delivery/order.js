/*
 * TSB - order.js
 * 
 * handles all condom ordering aspects
 *
 */



var mongoose = require('mongoose');
var crypto = require('crypto');

var Order = require('./models').Order;
var User = require('../user/models').User;

var sendout = require('../support/sendout');

var shortid = require('shortid');

exports.request = function (session_token, dorm_name, dorm_room, delivery_type, callback) {

    var dn = dorm_name;
    var dr = dorm_room;
    var dt = delivery_type;

    var now = new Date();
    var oid = shortid.generate();

    var device_uuid;
    //get the user's device_uuid
    User.find ({session_token : session_token}, function(err, users) {
	if (users.length == 0) {
	    callback({'response': 'DELIVERY_REQUEST_ERROR_USER_NOT_FOUND'}, 400);
	} else {
	    device_uuid = users[0].device_uuid;
	   
	    Order.find({order_number:oid}, function (err, orders) {

			if (orders.length == 0) {
			    var new_order = new Order({
					order_number : oid, 

					requester : device_uuid, 
					deliverer : "",
					
					order_received : true, 
					order_accepted : false,
					order_delivered : false,
					order_failed : false,
					
					date_requested: now, 
					date_accepted : null, 
					date_delivered: null, 

					delivery_estimate : -1,

					delivery_destination : {
					    dorm_name : dorm_name, 
					    dorm_room : dorm_room, 
					    delivery_type : delivery_type, 
					    coordinates : {
						lat: 0, 
						lng: 0,
					    }
					}
				
			    });

			    //order doesn't exist, so let's create it
			    new_order.save(function (err) {
				if (err) {
				    console.log('Error saving new order: ' + err);
				}

				sendout.request_alert_sendout(dorm_name);

				callback({'response': "DELIVERY_REQUEST_SUCCESS",
					  'order_number': oid}, 
				 	 201);
			    });
			} else {
			    callback({'response':"DELIVERY_REQUEST_ERROR_DATABASE_ERROR"}, 500);
			}

	    });

	}
    });	
}


exports.status = function(order_number, callback) {

    var oid = order_number;

    Order.find({order_number:oid}, function (err, orders) {
	var len = orders.length;


	if (len == 0) {
	    // the order doesn't exist
	    callback({'response':'DELIVERY_STATUS_ERROR_ORDER_NOT_FOUND'},
	    		   400);
	} else {
	    var or = orders[0];
	    var order_accepted = or.order_accepted;
	    var order_delivered = or.order_delivered;
	    var order_failed = or.order_failed;
	    
	    var date_accepted = or.date_accepted;
	    var date_delivered = or.date_delivered;
	    var delivery_estimate = or.delivery_estimate;

	    callback({
		'response' : 'DELIVERY_STATUS_SUCCESS',
		'order_number' : oid,
		
		'order_accepted' : order_accepted,
		'order_delivered' : order_delivered,
		'order_failed' : order_failed,
		
		'date_accepted' : date_accepted,
		'date_delivered' : date_delivered,
		
		'delivery_estimate' : delivery_estimate,
		
		}, 
		200);
	}


    });

}

exports.all = function(callback) {
	Order.find( function (err, orders){
		
		if (err) {
			callback('DELIVERY_REQUEST_ALL_ERROR_DATABASE_ERROR', 500);
		} else {
			var all = [];

			for (i in orders) {
				order_dict = orders[i];
				this_order = {
					'requester' : order_dict.requester,
					'deliverer' : order_dict.deliverer,

					'order_number' :  order_dict.order_number,
					
					'order_accepted' : order_dict.order_accepted,
					'order_delivered' : order_dict.order_delivered,
					'order_failed' : order_dict.order_failed,
					
					'date_requested' : order_dict.date_requested,
					'date_accepted' : order_dict.date_accepted,
					'date_delivered' : order_dict.date_delivered,
					
					'delivery_estimate' : order_dict.delivery_estimate,

					'delivery_destination' : order_dict.delivery_destination
				}
				all.push(this_order);
			}

			callback({'response':'DELIVERY_REQUEST_ALL_SUCCESS',
					  'orders': all}, 200);
		}

	});

}

exports.accept = function(session_token, order_number, delivery_estimate, callback) {

	//get the user's device_uuid
    User.find ({session_token : session_token}, function(err, users) {
		if (users.length == 0) {
		    callback({'response': 'DELIVERY_REQUEST_ACCEPT_ERROR_USER_NOT_FOUND'}, 400);
		} else { 
			var now = new Date();
			var deliverer = users[0].device_uuid;
			Order.findOneAndUpdate({order_number : order_number}, 
								   {order_accepted:true, 
								   	deliverer : deliverer,
								    date_accepted : now, 
								    delivery_estimate : delivery_estimate }, function(err) {
										if (err) {
											console.log(err);
										}
										callback({'response':'DELIVERY_REQUEST_ACCEPT_SUCCESS'}, 
												  200);
									});
		}

	});

}
	    
exports.deliver = function(session_token, order_number, callback) {

	//get the user's device_uuid
    User.find ({session_token : session_token}, function(err, users) {
		if (users.length == 0) {
		    callback({'response': 'DELIVERY_REQUEST_DELIVER_ERROR_USER_NOT_FOUND'}, 400);
		} else { 
			var now = new Date();
			var deliverer = users[0].device_uuid;
			Order.findOneAndUpdate({order_number : order_number}, 
								   {order_delivered: true,
								    order_accepted : true, // in case it wasn't 
								    date_delivered : now}, function(err) {
										if (err) {
											console.log(err);
										}
										callback({'response':'DELIVERY_REQUEST_DELIVER_SUCCESS'}, 
												  200);
									});
		}

	});

}
	    
