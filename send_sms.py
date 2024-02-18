# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = ['AC0e1cab751217f564c29270344af20b60']
auth_token = ['06c40737f6ca8f0ccb8086adab492418']
client = Client(account_sid, auth_token)

message = client.messages.create(
                              to='+13022526216',
                              from_='+18667403511',
                              body='Hi there'
                          )

print(message.sid)