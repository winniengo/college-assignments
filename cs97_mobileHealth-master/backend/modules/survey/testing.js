/*
 * TSB - Survey/Testing.JS file
 * Tests for the survey module. 
 */


var mongoose = require('mongoose');
var SurveyPrototype = require('./models').SurveyPrototype;
var Survey = require('./models').Survey;
var Campaign = require('./models').SurveyCampaign;
var User = require('../user/models').User;

// import crontab here too



exports.create_test_campaign = function (callback) {

	
	var new_survey_prototype = new SurveyPrototype({
		survey_id : '123456789',
	    survey_title : 'Survey1',

	    // the actual questions
	    survey_body : [ {question_id : '1', question_title: 'Your Yoghurt', 
	    				 question: 'Do you like yoghurt?',
	    				 response: ''},
	    				 {question_id : '2', question_title: 'Your Yoghurt 2', 
	    				 question: 'Are you sure?',
	    				 response: ''},
	    				 {question_id : '3', question_title: 'Your Yoghurt 3', 
	    				 question: 'Like really?',
	    				 response: ''},
	    			  ],

	});
	

	console.log('test');


	new_survey_prototype.save();


	var u_id;
	var q = User.where({device_uuid:'328fb58d8a279160'});
	q.findOne(function(err, user){
		if (err) {
			console.log("couldn't get user 123456");
		} 
		if (user) {
			u_id = user._id;
			console.log('u_id: ' + u_id);

			var new_campaign = new Campaign({

				campaign_id : "TestCampaign1",
		        campaign_title : "I am testing the campaign feature", 

		        prototype_survey_id : new_survey_prototype._id, 
		        completed_survey_ids : [],

		        eligible_users : [u_id],
		        pending_users : [],
		        completed_users : [],

		        crontab : "* * * * * *", //the crontab on which this campaign gets executed

		    });
		    
		    // TODO : Somehow incorporate a campaign end date
	        new_campaign.save();

	        callback({'response' : 'all done'}, 200);

		} else {
			console.log('user not found');
		}
	});
}
