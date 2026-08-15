from twilio.rest import Client
account_sid = 'AC4b506aba7d42025116d6bf5d0ba75740'
auth_token = 'accf60c68aaee4bac40f80d132a7b1b4'
client = Client(account_sid, auth_token)
message = client.messages.create(
    to='+18777804236',
    from_='+14472442830',  # your Twilio number, in E.164 format
    body='Test message'
)
print(message.sid)