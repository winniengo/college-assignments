/* 
 * TSB - Register.js
 */

var mongoose = require('mongoose');
var crypto = require('crypto');
var User = require('./models').User;


exports.register = function(device_uuid, passphrase, signup_token, device_os, 
							push_id, callback) {
    var u = device_uuid;
    var p = passphrase;
    var st = signup_token.replace(/\s/g, ""); //strip whitespace
    var dos = device_os;


    // check that the signup_token is correct
    if (st != "tsb2014") {
		console.log("TSBToken incorrect, token was:", st);
    	callback({'response': 'REGISTER_ERROR_INVALID_SIGNUP_TOKEN'}, 401);
    } else {
    	// do crypto to hash passphrase and generate auth_token
    
	    var iter = 1000 //num iterations of Hash function

	    /*
	      TODO: Reinstate Salt
	    try {
		var s = crypto.randomBytes(10).toString('hex');
	    } catch (ex) {
		// problem generating the salt, should handle this
		console.log("problem generating salt in register()");
	    }
	    */
	    var s = '123'

		crypto.pbkdf2(p, s, iter, 128, function(err, key) {
			if (err) {
				callback({'response' : 'REGISTER_ERROR_HASHING_ERROR'}, 500);
			} else {
				
				var hp = key.toString('hex');

				// generate an initial session token and set expiry date
			    var t = crypto.randomBytes(128).toString('hex');
			    
			    var now = new Date();
			    var t_expiration = new Date(now);
			    t_expiration.setHours(now.getHours() + 6);
			    

			    var d = new Date();
			    var new_user = new User({
					device_uuid : u, 
					device_os : dos,
					
					hashed_passphrase : hp, 
				    salt : s,
					
					session_token : t,
					session_token_expires : t_expiration,
					
					register_date : d,

					role: 'USER', //sets the user for default user privileges

					push_id : push_id

			    });


				//check if user exists
			    User.find({ device_uuid : u }, function (err, users) {
			    	console.log('users: ' + users);
			    	if (err) {
			    		console.log(err);
			    		callback({'response':'REGISTER_ERROR_DATABASE_ERROR'}, 500);
			    	} else {
			    		if(users.length == 0) {
						    //user doesn't exist yet
						    new_user.save(function (err) {
								if (err) {
								    console.log('Error saving new user: ' + err);
								    callback({'response':'REGISTER_ERROR_DATABASE_ERROR'}, 
								    	500);
								} else {
									callback({'response':"REGISTER_SUCCESS",
									  'session_token': t,
									  'session_token_expires' : t_expiration, 
									}, 
									200);		
								}

							});
						} else {
					    callback({'response':'REGISTER_ERROR_DEVICE_ALREADY_REGISTERED'},
					    		412);
						}

			    	}

			    });

			}

		});

    }
	    

}
