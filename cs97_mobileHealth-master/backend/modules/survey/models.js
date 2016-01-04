/*
 * TSB - Survey/Models.JS file
 * Defines the TSB Backend's database models for survey aspects
 */

var mongoose = require('mongoose');
var Schema = mongoose.Schema;
var User = require('../user/models').User;


var prototypeSurveySchema = mongoose.Schema({
    
    survey_id : String,
    survey_title : String,

    // the actual questions
    survey_body : [ {question_id : String, question_title: String, question: String, response: String} ],

});

var surveyCampaignSchema = mongoose.Schema({
        campaign_id : String,
        campaign_title : String, 

        prototype_survey_id : {type: Schema.ObjectId, ref: 'prototypeSurveySchema'}, 
        completed_survey_ids : [{type: Schema.ObjectId, ref: 'surveySchema'}],

        eligible_users : [{type: Schema.ObjectId, ref: 'userSchema'}],
        pending_users : [{type: Schema.ObjectId, ref: 'userSchema'}],
        completed_users : [{type: Schema.ObjectId, ref: 'userSchema'}],

        survey_link : String,

        crontab : String, //the crontab on which this campaign gets executed

        // TODO : Somehow incorporate a campaign end date

});


var surveySchema = mongoose.Schema({
    
    campaign_id : {type: mongoose.Schema.ObjectId, ref: 'surveyCampaignSchema'},

    survey_id : String,
    survey_title : String,

    participant_device_uuid : String, //uuid of the requesting device
    participant_most_recent_order_number : String,

    // specifics
    survey_body : [ {question_id : String, question_title:String, question: String, response: String} ],

});


// export the different schemas as models
module.exports = {
    SurveyPrototype : mongoose.model('SurveyPrototype', prototypeSurveySchema),
    Survey : mongoose.model('Survey', surveySchema),
    SurveyCampaign : mongoose.model('SurveyCampaign', surveyCampaignSchema),
};
