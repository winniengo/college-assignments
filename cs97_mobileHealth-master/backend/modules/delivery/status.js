/*
 * TSB - status.js
 * 
 * gives the status for a current condom delivery
 *
 */


var mongoose = require('mongoose');
var crypto = require('crypto');

var Order = require('./models').Order;
var User = require('../user/models').User;

var shortid = require('shortid');


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
