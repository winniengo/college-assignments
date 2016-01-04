/*
 * TSB - db/db.js - controls interactions with the MongoDB database
 */

var mongoose = require('mongoose');

var dbURI = 'mongodb://localhost:27017/tsb-db';

mongoose.connect(dbURI);


mongoose.connection.on('connected', function() {
		console.log('Mongoose default connection open to: ' + dbURI);
});

mongoose.connection.on('error', function (err) {
		console.log('Mongoose default connection encountered error: ' + err);
});


mongoose.connection.on('disconnected', function () {
		console.log('Mongoose default connection disconnected.');
});

process.on('SIGINT', function() {
		mongoose.connection.close( function() {
				console.log("Mongoose default connection disconnected after app received SIGINT");
		});
		process.exit(0);
});


// INCLUDE ANY SCHEMAS AND MODELS HERE
//require('../user/models.js').User;
//require('../delivery/models.js').Order;
