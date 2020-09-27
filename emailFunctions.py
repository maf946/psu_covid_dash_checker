import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email_update(test_mode, overall_total_positive, sendgrid_api_key):
    from_email = settings.from_email
    to_email = settings.to_email
    subject_prefix = settings.subject_prefix
    subject = subject_prefix + str(overall_total_positive)
    if (test_mode):
        subject = "TEST MODE: " + subject
    html_content='See <a href=\"' + settings.url + '\">complete dashboard</a> for more information.'

    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=html_content)
    try:
        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(message)
    except Exception as e:
        print(e)
