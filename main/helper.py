import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_verification_email(recipient_email, verification_link):
    sender = 'official@themagicspice.in'
    sender_password = '1Ashish1joseph1#'
    sender_title = "Administrator-theMagicSpice"

    greeting = "Hello!"
    button_html = f'<a href="{verification_link}" style="background-color: #4CAF50; border: none; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px;">Verify Account</a>'
    html_content = f"""
    <html>
      <body>
        <p>{greeting}</p>
        <p>Please click the button below to verify your account:</p>
        {button_html}
      </body>
    </html>
    """

    msg = MIMEMultipart('alternative')
    msg.attach(MIMEText(html_content, 'html'))

    msg['Subject'] = "Account Verification"
    msg['From'] = f"{sender_title} <{sender}>"
    msg['To'] = recipient_email

    try:
        server = smtplib.SMTP_SSL('smtppro.zoho.in', 465)
        server.login(sender, sender_password)
        server.sendmail(sender, recipient_email, msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")
