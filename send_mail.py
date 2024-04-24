import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailSender:
    def __init__(self, sender_email, sender_password):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.recipient_email_QC = ['krishnavalliappan02@gmail.com', "madhumithaj2000@gmail.com", "lakshminarasimhan.lnr@gmail.com"]
        self.recipient_email_BC = ["meeramnair99@gmail.com", "mkrishnanunni03@gmail.com", "krishnavalliappan02@gmail.com"]
        # self.recipient_email_BC = ["krishnavalliappan02@gmail.com", "krishnavalliappan24@gmail.com"]
        self.amazon_link = "https://hvr-amazon.my.site.com/BBIndex"
    
    def split_places(self, places):
        # splitplaces one by one send in the email body
        text = ""
        for i in places:
            text += f"{i}\n"
        return text

    def send_email(self, places, province="QC"):
        if province == "QC":
            receiver_email = self.recipient_email_QC
            subject = '‼‼ Urgent: Amazon a job opening in Quebec Canada'
        elif province == "BC":
            receiver_email = self.recipient_email_BC
            subject = '‼‼ Urgent: Amazon a job opening in British Columbia Canada'
        else:
            return "Invalid province"
        message = f"""Opening in following places: \n
                {self.split_places(places)}
                Link to apply: {self.amazon_link}"""
        
        email_message = MIMEMultipart()
        email_message['From'] = self.sender_email
        email_message['To'] = ", ".join(receiver_email)
        email_message['Subject'] = subject
        # Add the message body
        email_message.attach(MIMEText(message, 'plain'))

        # SMTP server configuration
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = self.sender_email
        smtp_password = self.sender_password
        
        # Create a secure connection with the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(email_message)
        
        return f"Email sent to following places: \n {self.split_places(places)} to following users: \n{receiver_email}"
        

