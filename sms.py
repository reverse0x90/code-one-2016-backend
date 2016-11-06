from flask import Flask, request, redirect
#import requests
import twilio.twiml
import cPickle as pickle
import json
import urllib2


app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def reply_payment():
    """Respond and greet the caller by name."""

    url = 'http://localhost/update/chore/status/complete'
    message_body = request.values.get('Body', None)

    if "Approve" in message_body or "approve" in message_body or "Accept" in message_body or "accept" in message_body:
         # Save and update the chore status
        pickle_file = open('chore_state.p', 'rb') 
        status_stack = pickle.load(pickle_file)
        chore_vars = status_stack.pop()
        pickle_file.close()

        pickle_file = open('chore_state.p', 'wb')
        pickle.dump(status_stack, pickle_file)
        pickle_file.close()

        chore_vars["status"] = "completed"
        payload = {"username": chore_vars["username"], "title": chore_vars["title"], "status": chore_vars["status"]}
        data = json.dumps(payload)
        req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
        f = urllib2.urlopen(req)
        response = f.read()
        f.close()

        print "[+] Payment for %s completing the chore %s has been approved" % (chore_vars["username"].title(), chore_vars["title"])
        reply_message = "Thank you for using First National Bank your the chore payment for %s completing the chore %s has been approved and the funds have been successfully transfered." % (chore_vars["username"].title(), chore_vars["title"])

    elif "Deny" in message_body or "deny" in message_body:
        print str("I am in deny " + message_body)
        # Save and update the chore status
        pickle_file = open('chore_state.p', 'rb')
        status_stack = pickle.load(pickle_file)
        pickle_file.close()

        chore_vars = status_stack.pop()

        pickle_file = open('chore_state.p', 'wb')
        pickle.dump(status_stack, pickle_file)
        pickle_file.close()

        chore_vars["status"] = "not-completed"
        payload = {"username": chore_vars["username"], "title": chore_vars["title"], "status": chore_vars["status"]}
        data = json.dumps(payload)
        req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
        f = urllib2.urlopen(req)
        response = f.read()
        f.close()

        print "[+] Payment for %s completing the chore %s has been denied" % (chore_vars["username"].title(), chore_vars["title"])
        reply_message = "Thank you for using First National Bank your chore payment for %s completing the chore %s has been denied and no funds have been transfered." % (chore_vars["username"].title(), chore_vars["title"])
    else:
        # Save and update the chore status
        pickle_file = open('chore_state.p', 'rb')
        status_stack = pickle.load(pickle_file)
        pickle_file.close()

        chore_vars = status_stack.peek()

         print "[+] Response unknown. Message body was: %s" % (message_body)
        reply_message = "I am sorry I didn't understand your response. Please reply Approve or Deny the requested payment for %s completing the chore %s." % (chore_vars["username"].title(), chore_vars["title"])
    
    resp = twilio.twiml.Response()
    resp.message(reply_message)

    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)