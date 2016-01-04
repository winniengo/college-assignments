/*
 * TSB - sendout.JS file 
 * Functions to send out push notifications via GCM (and APN)
 */




 var gcm = require('node-gcm');
 var Promise = require('bluebird');
 var async = require('async');


 // models we need
 var Campaign = require('../survey/models.js').SurveyCampaign;
 var User = require('../user/models.js').User;


 exports.survey_sendout = function(push_id_list, campaign_id) {

 	var sender = new gcm.Sender('AIzaSyChUqVv6OSHR58eElHGTYOYJj3IbXgCZ5Y');

 	// or with object values
	var message = new gcm.Message({
	    collapseKey: 'DingDong:Condom',
	    delayWhileIdle: true,
	    timeToLive: 3,
	    data: {
	    	type: 'survey',
	        campaign_id : campaign_id,	    
		}
		
	});
     console.log('in survey_sendout:');
	fetchAllEligibleUserPushIDs (campaign_id, function(push_ids) {
		console.log('in survey_sendout, ids: ' + push_ids);
		if (!push_ids) {
			callback('No eligible users to send out', 'none sent');
		} else {
			console.log('sending to: ' + push_ids);
			sender.send(message, push_ids , 4, function(err, result) {
				if (err) {
					console.log(campaign_id + 'Sender err: ' + err);
				} else {
					console.log('GCM Sender: ' + result);
				} 
				
			});
		}
	});
		
 }


function fetchAllEligibleUserPushIDs (campaign_id, callback) {
	// send a GCM notification to everyone 

	var push_ids = [];

	Campaign.findOne({ campaign_id : campaign_id }, function(err, campaign){
 		if (err) {
 			console.log('(Sendout.js): Error: ' + err);
 		}
		if (campaign) {

 			var eligible_users = campaign.eligible_users;
			
 			async.map(eligible_users, function(user_id, done) {
 				User.findOne({_id : user_id}, function (err, user){
					if (err) {
						console.log('in set_announcement: ' + err);
				
					}
				    if (user) {
						var id = user.push_id;
						if (id) {
						   
						    done(null, id);
						}
					} else {
					    done(null, null);
					}
				});
 			}, function(err, push_ids) {
 			    if(err) {
 				console.log('error in fetchAllEligibleUserPushIDs: ' + err);
 			    }
 			    callback(push_ids);
 			});			
		}
	});
}



exports.do_post_order_sendout = function () {

	Campaign.findOne({campaign_id:"POST_ORDER_CAMPAIGN"}, function(err, campaign){
		var eligible_users = campaign.eligible_users;

		module.exports.survey_sendout(eligible_users, "POST_ORDER_CAMPAIGN");

	});

}


exports.initialize_post_order_campaign = function (callback) {

	Campaign.findOne({campaign_id: 'POST_ORDER_CAMPAIGN'}, function(err, campaign) {

		if (err) {
			console.log('Error in initialize_post_order_campaign: ' + err);
		}
		if (campaign) {
			console.log('Post-Campaign for Android exists, is: ' + campaign.campaign_id);
		} else {
			var new_campaign = new Campaign({

				campaign_id : 'POST_ORDER_CAMPAIGN',
		        campaign_title : 'POST_ORDER_CAMPAIGN', 

		        eligible_users : [],
		        pending_users : [],
		        completed_users : [],

		        survey_link : 'https://docs.google.com/forms/d/1za7RHK4dhrIneY_XwkjQdOnBBi5CByW5sV4iCD-8xn0/viewform',

		        crontab : "* * * * *", //the crontab on which this campaign gets executed
				});

			new_campaign.save(function(err){
				if (err) {
					console.log('Error saving a new announcement: ' + err);
				} else {
					console.log('New Android annoucement saved: ' + new_campaign);
				}
			});
		}

	});

}


exports.request_alert_sendout = function(dorm) {
	var sender = new gcm.Sender('AIzaSyChUqVv6OSHR58eElHGTYOYJj3IbXgCZ5Y');
	// should be a separate GCM entity

	// create a new message
	var message = new gcm.Message({
	    collapseKey: 'DingDong:Deliverer',
	    delayWhileIdle: true,
	    timeToLive: 3,
	    data: {
	    	type: 'request',
	        dorm : dorm,
		}
		
	});

	User.find({role:'ADMIN'}, function(err, admins) {
		if (err) {
			console.log('Errors in request_alert_sendout: ' + err);
		} else if (admins) {
			for (i=0;i<admins.length;i++) {
				if (admins[i].push_id) {
					sender.send(message, [admins[i].push_id], 4, function(err, result){
						if (err) { console.log('error alerting admin') 
						} else { console.log('alert sender: ' + result);}
					});
				} else {
					console.log('admin ' + admins[i].device_uuid + ' has no push_id');
				}
			}
		} else {
			console.log('Errors in request_alert_sendout: No admins found');
		}

	});


}


exports.delivery_sendout = function(user_id, status) {
	var sender = new gcm.Sender('AIzaSyChUqVv6OSHR58eElHGTYOYJj3IbXgCZ5Y');

 	// or with object values
	var message = new gcm.Message({
	    collapseKey: 'DingDong: Condom!',
	    delayWhileIdle: true,
	    timeToLive: 3,
	    data: {
	    	type: 'delivery', 
	    	status: status   
		}
		
	});

	User.findOne({_id: user_id}, function(err, user) {
		if (err) {
			console.log('Error in delivery_sendout: ' + err);
		} else if (user) {
			var push_id = user.push_id;
			if (push_id) {
				sender.send(message, [push_id] , 4, function(err, result) {
					if (err) {
						console.log("delivery_sendout: sender err: " + err);
					} 
				});
			} else {
				console.log("User " + user.device_uuid + " does not have a push_id");
			}

		} else {
			console.log("User not found");
		}

	});
		
}


exports.do_test_sendout =  function (callback) {

	Campaign.findOne({campaign_id:"TestCampaign1"}, function(err, campaign){
		var eligible_users = campaign.eligible_users;

		module.exports.survey_sendout(eligible_users, "TestCampaign1", function(err, result) {
			console.log('eligible users: ' + eligible_users);
			console.log('sender result: '+ result);
			if (err) {
				console.log('err: ' + err);
			}
		})
	});

}
