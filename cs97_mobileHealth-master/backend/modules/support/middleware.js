/*
 * TSB - Middleware.JS file 
 * Useful middleware for the TSB project
 */


var mongoose = require('mongoose');
var User = require('../user/models').User;
var Order = require('../delivery/models').Order;



exports.get_device_uuid = function (req, res) {
	var token = req.body.session_token

	User.find ({session_token : token}, function(err, users) {
		if (users.length == 0) {
			res.status(401).json({'response':"ERROR_NOT_AUTHENTICATED"});
		} else {
			return users[0].device_uuid;
		}
	});

}

//check if a user is authenticated, otherwise redirect them to a 403 page

exports.is_authenticated = function (req, res, next) {

	// check if the user is authenticated (i.e. provides a session token)
	var token = req.body.session_token;
        
	// check if that token is valid
	User.find ({session_token : token}, function(err, users) {
		if (users.length == 0) {
			res.status(401).json({'response':"ERROR_NOT_AUTHENTICATED"});
		} else {
			return next();
		}
	});

}

exports.is_authenticated_and_requester = function (req, res, next) {

	// check if the user is authenticated (i.e. provides a session token)
	var token = req.body.session_token;
	var order_number = req.body.order_number;

	// check if that token is valid
	User.find ({session_token : token}, function(err, users) {
		if (users.length == 0) {
			res.status(401).json({'response':"ERROR_NOT_AUTHENTICATED"});
		} else {
			var device_uuid = users[0].device_uuid;
			Order.find( {order_number : order_number} , function(err, orders) {
				if (orders.length == 0) {
					res.status(404).json({'response':"ERROR_ORDER_NOT_FOUND"});
				} else {
					console.log('rq:' + orders[0].requester + '  duuid: ' + device_uuid);
					if (orders[0].requester == device_uuid) {
						return next();
					} else {
						res.status(403).json({'response':'ERROR_FORBIDDEN'});
					}
				}

			});
		}
			
	});

}


exports.is_authenticated_and_eligible = function (req, res, next) {

	// check if the user is authenticated (i.e. provides a session token)
	var token = req.body.session_token;

	// check if that token is valid
	User.find ({session_token : token}, function(err, users) {
		if (err) {
			console.log(err);
			res.status(500).json({'response':'DELIVERY_REQUEST_ERROR'});
			return;
		}
		if (users.length == 0) {
			res.status(401).json({'response':"ERROR_NOT_AUTHENTICATED"});
		} else {
			if (err) {
				console.log(err);
				res.status(500).json({'response':'DELIVERY_REQUEST_ERROR'});
				return;
			}

			var device_uuid = users[0].device_uuid;

			Order.find( { requester : device_uuid } , function(err, orders) {
				if (orders.length == 0) {
					next();
				} else {

					var now = new Date();
					var now_string = now.toDateString();
					var date_string;

					for (i in orders) {
						date_string = new Date(orders[i].date_requested).toDateString();
						if (date_string == now_string) {
							if (!orders[i].order_failed) {
								res.status(429).json({'response':"DELIVERY_REQUEST_ERROR_TOO_MANY_REQUESTS"});
								return;
							}
						}
					
					}
					next();
				}

			});
		}
			
	});

}

exports.is_authenticated_and_admin = function (req, res, next) {

	// check if the user is authenticated (i.e. provides a session token)
	var token = req.body.session_token;

	// check if that token is valid
	User.find ({session_token : token}, function(err, users) {
		if (users.length == 0) {
			res.status(401).json({'response':"ERROR_NOT_AUTHENTICATED"});
		} else {
			if (users[0].role != 'ADMIN'){
				res.status(403).json({'response':"ERROR_NOT_PRIVILEGED"});
			} else {
			return next();
			}
		}
	});
}