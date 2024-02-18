from sinch import Client

sinch_client = Client(
    key_id="db1aa87a-bd62-4bb8-8ba5-56d37b5bf4ee",
    key_secret="a.EJur9KQ55mD7E.Lw6iQxSeFn",
    project_id="5fb58ea0-10d4-4227-b71d-c0bbc32986b4"
)

def send_message():
    send_batch_response = sinch_client.sms.batches.send(
    body="Fall detection alert: Room 207 at Bed B! \n\n - Automated message sent from CareSentry API",
    to=["13022526216"],
    from_="12085810360",
    delivery_report="none"
)

send_message()