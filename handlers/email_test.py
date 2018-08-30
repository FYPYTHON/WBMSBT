from exchangelib import DELEGATE, Account, Credentials, Message, Mailbox, HTMLBody
sender = "Faye.Wang@autoflight.com"
password = "WGQ_039103"
def Email(to, subject, body):
    creds = Credentials(
        username=sender,
        password=password
    )
    account = Account(
        primary_smtp_address='Faye.Wang@autoflight.com',
        credentials=creds,
        autodiscover=True,
        access_type=DELEGATE
    )
    m = Message(
        account=account,
        subject=subject,
        body=HTMLBody(body),
        to_recipients = [Mailbox(email_address=to)]
    )
    try:
        m.send()
        print("send ok")
    except Exception as e:
        print(e)
if __name__ =="__main__":

    Email("Faye.Wang@autoflight.com", "AutoFlight", "code")