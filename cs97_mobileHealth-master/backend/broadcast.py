import urllib
import httplib


SESSION_TOKEN = "67f4e18a13031f7c3f51477495c87f2a76fa2224664022b5555472c09a189c991fc081e0518ee07cfbe90f46cc11f7508f0b7187f82c6e37f8b0c4ff8210cc5f"

def main():

	print "This will send out a broadcast message to all TSB users"

	message = raw_input('Enter the message to be broadcast:\n\n>>')

        print "Please input yes for if we're delivering or no if not:\n\n"

        raw_delivery = raw_input(">>")

        if raw_delivery == "yes" or raw_delivery == "no":
                deliver = raw_delivery
                send_broadcast(message, deliver)
        else:
                print "Error in parsing your input. Try again"

        
        


def send_broadcast(message, delivering):


	data = urllib.urlencode({'message': message, 'open_for_business' : delivering, 'session_token': SESSION_TOKEN})

	h = httplib.HTTPConnection('localhost:8080')

	headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

	h.request('POST', '/api/broadcast/announcement/set', data, headers)

	r = h.getresponse()

	print r.read()


main()

