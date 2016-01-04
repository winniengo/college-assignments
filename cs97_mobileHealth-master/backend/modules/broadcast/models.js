/*
 * TSB - models for the appwide broadcast 
 */

var mongoose = require('mongoose');
var Schema = mongoose.Schema;


var announcementSchema = mongoose.Schema({
	announcement_id : String,
	open_for_delivery : Boolean,
	message : String, 
});

module.exports = {
	Announcement : mongoose.model('Announcement', announcementSchema)
};