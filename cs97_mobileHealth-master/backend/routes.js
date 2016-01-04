/*
 * TSB - Routes.JS file 
 * Defines the overall form of our API
 */

// middleware module
var middleware = require('./modules/support/middleware');

// user modules
var register = require('./modules/user/register');
var login = require('./modules/user/login');

// delivery modules
var order = require('./modules/delivery/order');
var deliverer = require('./modules/delivery/deliverer');
var status = require('./modules/delivery/status');

// survey modules
var retrieve = require('./modules/survey/retrieve');
var complete = require('./modules/survey/complete');
var survey_test = require('./modules/survey/testing');

// GCM sendout module
var sendout = require('./modules/support/sendout');

// broadcast
var announce = require('./modules/broadcast/announce');


module.exports = function(app) {


    app.get('/', function(req, res) {
		res.end("TSB Backend v0.1");
    });


    // authenticate with the backend by supplying
    //   - a persistent device uuid
    //   - an auth_token that was given by the backend
    app.post('/api/login',function(req,res){

	console.log("in /api/login, request: ", req.body);

	var uuid = req.body.device_uuid;
	var passphrase = req.body.passphrase;
	var push_id = req.body.push_id;

	
		login.login(uuid, passphrase, push_id, function (result, status) {
		    console.log(result + 'status: ', status);
		    res.status(status).json(result);
		});
    
    });
    

    // register with the backend by supplying 
    //     - a (persistent) device uuid
    //     - a signup_code that is distributed to each user
    app.post('/api/register', function(req,res) {
	
	var device_uuid = req.body.device_uuid;
    var passphrase = req.body.passphrase;
	var signup_token = req.body.signup_token;
	var device_os = req.body.device_os;
	var push_id = req.body.push_id;
	
	register.register(device_uuid, passphrase, signup_token, device_os, push_id, function (result, status) {
	    console.log(result);
	    res.status(status).json(result);
		});
    });


    // request a delivery 
    app.post('/api/delivery/request', middleware.is_authenticated_and_eligible, function(req, res) {
	var session_token = req.body.session_token;
	var dorm_name = req.body.dorm_name;
	var dorm_room = req.body.dorm_room;
	var delivery_type = req.body.delivery_type;
	
	order.request(session_token, dorm_name, dorm_room, delivery_type, function (result, status) {
				  console.log(result, status);
				  res.status(status).json(result);
		      });
    });

    // get the delivery status

    app.post('/api/delivery/status', middleware.is_authenticated_and_requester, function(req, res) {
	var session_token = req.body.session_token;
	var order_number = req.body.order_number;
	
	status.status(order_number, function (result, status) {
	    console.log(result);
	    res.status(status).json(result);
		});

    });


   	// get a list of all requests
   	app.post('/api/delivery/request/all', middleware.is_authenticated_and_admin, function(req, res) {
	
	deliverer.all(function (result, status) {
	    console.log(result);
	    res.status(status).json(result);
		});

    });

    // accept a request
   	app.post('/api/delivery/request/accept', middleware.is_authenticated_and_admin, function(req, res) {

   	var session_token = req.body.session_token;
   	var order_number = req.body.order_number;
   	var delivery_estimate = req.body.delivery_estimate;

	console.log('accept: '+ req.body);
	console.log('accept2: '+ req.body.delivery_estimate);

	deliverer.accept(session_token, order_number, delivery_estimate, function (result, status) {
	    console.log(result);
	    res.status(status).json(result);
		});

    });


    // accept a request
   	app.post('/api/delivery/request/deliver', middleware.is_authenticated_and_admin, function(req, res) {

   	var session_token = req.body.session_token;
   	var order_number = req.body.order_number;
   	
	deliverer.deliver(session_token, order_number, function (result, status) {
	    console.log(result);
	    res.status(status).json(result);
		});

    });

	
	// fail a request
   	app.post('/api/delivery/request/fail', middleware.is_authenticated_and_admin, function(req, res) {

   	var session_token = req.body.session_token;
   	var order_number = req.body.order_number;
   	
	deliverer.fail(session_token, order_number, function (result, status) {
	    console.log(result);
	    res.status(status).json(result);
		});

    });


    // get a survey for a given campaign id

    app.post('/api/survey/retrieve', middleware.is_authenticated, function(req, res) {
	var session_token = req.body.session_token;
	var campaign_id = req.body.campaign_id;

	console.log('retrieve :' + req.body.campaign_id);	
	retrieve.retrieve(session_token, campaign_id, function (result, status) {
	    console.log(result);
	    res.status(status).json(result);
		});

    });


    // get a survey for a given campaign id

    app.post('/api/survey/complete', middleware.is_authenticated, function(req, res) {
	var session_token = req.body.session_token;
	var campaign_id = req.body.campaign_id;
	var answers = req.body.answers;

	console.log('in routes: ' + answers);
	
	complete.complete(session_token, campaign_id, answers, function (result, status) {
	    console.log(result);
	    res.status(status).json(result);
		});

    });


    app.post('/api/broadcast/announcement/set', middleware.is_authenticated_and_admin, function(req,res) {

    	var message = req.body.message;
    	console.log('msg: ' + message);
    	var open_for_business = req.body.open_for_business;

    	announce.set_announcement(message, open_for_business, function(result, status) {
    		console.log(result);
    		res.status(status).json(result);
    	});

    });

    app.post('/api/broadcast/announcement/get', middleware.is_authenticated, function(req,res) {

    	console.log('getting announcement');
    	announce.get_announcement(function(result, status) {
    		console.log(result);
    		res.status(status).json(result);
    	});

    });


    /*
    // for testing purposes
    app.get('/api/survey/create_test_campaign', function (req, res) {

    	survey_test.create_test_campaign(function(result, status) {
    		console.log(result);
    		res.status(200).json(result);
    	});

    });

    app.get('/api/survey/do_test_sendout', function (req, res) {

    	console.log('doing test sendout');
    	sendout.do_post_order_sendout(function(res, status){
    		console.log(res);
    		res.status(200).json(result);
    	});

    });
    */

};
