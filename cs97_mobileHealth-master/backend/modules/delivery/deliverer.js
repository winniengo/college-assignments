/*
 * TSB - deliverer.js
 * 
 * methods for the android_deliverer app
 *
 */


var mongoose = require('mongoose');
var crypto = require('crypto');

var Order = require('./models').Order;
var User = require('../user/models').User;
var Campaign = require('../survey/models').SurveyCampaign;

var sendout = require('../support/sendout.js')

var shortid = require('shortid');


exports.all = function(callback) {
	Order.find(function (err, orders){
		
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
				if (!this_order.order_delivered) {
					all.push(this_order);
				}
			}

			callback({'response':'DELIVERY_REQUEST_ALL_SUCCESS',
					  'orders': all}, 200);
		}

	});

}

exports.accept = function(session_token, order_number, delivery_estimate_string, callback) {

    var delivery_estimate = parseInt(delivery_estimate_string);

    if (!delivery_estimate) {
		delivery_estimate = -1;
    }

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

    // add the user to the eligible post order survey users
	Order.findOne({order_number: order_number}, function(err, order) {
		if (err) {
			console.log('In deliver: ' + err);
		}
		if (order) {

			var requester = order.requester;
			User.findOne({device_uuid : requester}, function(err, user) {
				if (err) {
					console.log('In deliver: ' + err);
				}
				if (user) {
					var id = user._id;

					// send delivery notificaiton
					sendout.delivery_sendout(id, "success");

					Campaign.findOne({campaign_id:'POST_ORDER_CAMPAIGN'}, function(err, campaign) { 
											  	if (err) {
											  		console.log('In deliver: ' + err);
											  	}
											  	if (campaign) {
											  		//check that use is only here once
											  		userEligible(campaign.eligible_users, user, function(res){
											  			if (res) {
											  				campaign.eligible_users.push(id);
											  				campaign.save();
											  			}
											  		});
											  		
											  	}

											  });
				}
			}); 
		}
	});


	// send out a push notification! 



}

function userEligible (array, user, callback) {

	var isNotEligible = array.some(function(current) {
		return current.equals(user._id);
	});

	if (isNotEligible) {
		callback(false);
	} else {
		callback(true);
	}

}



exports.fail = function(session_token, order_number, callback) {

    //get the user's device_uuid
    User.find ({session_token : session_token}, function(err, users) {
		if (users.length == 0) {
		    callback({'response': 'DELIVERY_REQUEST_FAIL_ERROR_USER_NOT_FOUND'}, 400);
		} else { 
			var now = new Date();
			var deliverer = users[0].device_uuid;
			Order.findOneAndUpdate({order_number : order_number}, 
								   {$set : {order_failed:true}}, function(err, order) {
										if (err) {
											console.log(err);
										} else if (order) {
											var requester = order.requester;
											User.findOne({device_uuid: requester}, function(err, user) {
												if (err) {
													console.log("Error in fail: " + err);
												} else if (user) {
													sendout.delivery_sendout(user._id, "fail");
												} else {
													console.log("Error in fail: couldn't find requesting user");
												}
											});
											callback({'response':'DELIVERY_REQUEST_FAIL_SUCCESS'}, 
												  200);
										}	
									});
		}

	});

}
