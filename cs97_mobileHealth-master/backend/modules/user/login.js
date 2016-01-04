/* 
 * TSB - Login.js
 */


var crypto = require('crypto');
var mongoose = require('mongoose');

var User = require('./models').User;


exports.login = function(device_uuid, input_passphrase, push_id, callback) {
	
    User.find( {device_uuid: device_uuid}, function (err, users) {
	
	if(users.length != 0){
	    var hashed_passphrase = users[0].hashed_passphrase;
	    var session_token = users[0].session_token;
	    var session_token_expires = users[0].session_token_expires;
	    
	    //var s = users[0].salt;
	    var salt = '123';

	    var iterations = 1000;	   

	    // generate hash from secret input
	    try {
			var input_hashed_passphrase = 
				crypto.pbkdf2Sync(input_passphrase, salt, iterations, 128).toString('hex');
		} catch (err) {
		//error lol
		console.log("error hashing in /login: " + err);
	    }

	    var user = users[0];

	    if (hashed_passphrase == input_hashed_passphrase){
	    	// TODO: generate new session token and reassign it appropriately:
			
	    	user.push_id = push_id;

	    	user.save(function(err){
	    		if (err) {
	    			console.log('in login (43): ' + err);
	    			callback({'response': 'LOGIN_ERROR_DATABASE_ERROR'}, 500);
	    		} else {
	    			callback({'response' : "LOGIN_SUCCESS",
					  'session_token' : session_token,
					  'session_token_expires' : session_token_expires,
				 	          }, 201);

	    		}
	    	});



	    } else {
			callback({'response' : "LOGIN_ERROR_INVALID_PASSPHRASE", },
				400);
	    }
	} else {
		    callback({'response':"LOGIN_ERROR_INVALID_DEVICE_UUID", },
			    400);
	}
	
    });
}


