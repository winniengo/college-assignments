/*
 * TSB - Survey/Complete.JS file
 * API call to complete a survey as JSON given a campaign ID. 
 */

var mongoose = require('mongoose');
var SurveyPrototype = require('./models').SurveyPrototype;
var Survey = require('./models').Survey;
var Campaign = require('./models').SurveyCampaign;
var User = require('../user/models').User;

exports.complete = function (session_token, campaign_id, answers, callback) {

	// find the user ref
    User.find ({session_token : session_token}, function(err, users) {
		if (users.length == 0) {
			callback({'response': 'SURVEY_COMPLETE_ERROR_USER_NOT_FOUND'}, 400);
		} else {
			var user = users[0];
			var device_uuid = users[0].device_uuid;

			// find the campaign document
			Campaign.find ({campaign_id:campaign_id}, function(err, campaigns) {
				if (users.length == 0) {
					callback({'response' : 'SURVEY_COMPLETE_ERROR_CAMPAIGN_NOT_FOUND'}, 404);
				} else {
					var campaign = campaigns[0];

					// find the survey text

					var survey_query = SurveyPrototype.where({ _id : campaign.prototype_survey_id });

					survey_query.findOne(function(err, survey) {
						if (err) {
							callback({'response' : 'SURVEY_COMPLETE_DATABASE_ERROR'}, 500);
						} 
						if (survey) {
							var survey_prototype = survey;

							// now add a survey object for this respective user
							var user_survey = new Survey({

								campaign_id : campaign._id,

							    survey_id : campaign.prototype_survey_id,
							    survey_title : survey_prototype.survey_title,

							    participant_device_uuid : device_uuid, //uuid of the requesting device
							    participant_most_recent_order_number : '',

							    survey_body : JSON.parse(answers)
							});

							user_survey.save(function(err){
								if (err) {
									console.log('in retrieve.js(123): ' + err);
									return callback({'response' : 'SURVEY_COMPLETE_DATABASE_ERROR'}, 500);
								} else {
									// move user to completed_users array

									var eligible_users = campaign.eligible_users;
									var pending_users = campaign.pending_users;
									var completed_users = campaign.completed_users;

									eligible_users.remove(user._id);
									pending_users.remove(user._id);
									completed_users.push(user._id);

									Campaign.save(function(err) {
										if (err) {
											console.log('in retrieve.js(139): ' + err);
											return callback({'response' : 'SURVEY_COMPLETE_DATABASE_ERROR'}, 500);
										} else {
											// return success code to the client
											callback({'response' : 'SURVEY_COMPLETE_SUCCESS'}, 201);
										}
									});

								} 

							});

							
						} else {
							callback({'response' : 'SURVEY_COMPLETE_ERROR_SURVEY_NOT_FOUND'}, 404);
						}

						
						
					});


				}
			});

		}
	});

}