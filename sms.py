from flask import Flask, request, redirect
import twilio.twiml

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def reply_payment():
    """Respond and greet the caller by name."""

    message_body = request.values.get('Body', None)

    if "Approve" or "Approve" in message_body:
        reply_message = "Thank you for using First National Bank your the chore payment for Evan has has been approved."
    elif "Deny" or "deny" in message_body:
        reply_message = "Thank you for using First National Bank your the chore payment for Evan has has been denied."
    else:
        reply_message = "I am sorry I did't understand your response. Please reply Approve or Deny."
    resp = twilio.twiml.Response()
    resp.message(reply_message)

    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)