import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import time

load_dotenv()

# The URL you will send the POST request to
url = 'https://hvr-amazon.my.site.com/BBIndex'

def main():
    # Send the GET request
    response = requests.get(url)

    if response.status_code != 200:
        print('Failed to send POST request')
    else:
        # Now you use Beautiful Soup to parse the response text
        soup = BeautifulSoup(response.text, 'html.parser')

        # Do something with the parsed HTML
        # For example, find an element with a specific id
        # element = soup.find(id='some_id')

        # Find all 'div' elements with class 'listing row'
        listing_rows = soup.find_all('div', class_='listing row')

        # Find all 'h6' elements that are descendants of something other than 'div.listing row'
        # Then find all 'span' elements within those 'h6' elements
        spans = []
        for listing_row in listing_rows:
            # We find all 'h6' that are not direct children of the 'listing_row'
            h6s = listing_row.find_all('h6')
            for h6 in h6s:
                # Now we check if 'span' is inside 'h6'
                spans_inside_h6 = h6.find_all('span')
                spans.extend(spans_inside_h6)

        text_to_match = "QC Canada"
        # text_to_match = "Y Germany"
        email = False
        places = []
        for span in spans:
            text_to_check = span.text[-9:]
            if text_to_check == text_to_match:
                email = True
                places.append(span.text)
                break

        if email:
            print("Sending email")
            send_email(places)

def send_email(mes):
    def message_list(mes):
        text=""
        for i in mes:
            text+=f"{i}\n"
        return text
    
    # Email configuration
    sender_email = os.environ["username"]
    receiver_email = 'krishnavalliappan02@gmail.com'
    subject = '‼‼ Urgent: Amazon a job opening in Quebec Canada'
    message = f"""Opening in following places: \n
                {message_list(mes)}
                Link to apply: {url}""" 
                
    # Create a multipart message
    email_message = MIMEMultipart()
    email_message['From'] = sender_email
    email_message['To'] = receiver_email
    email_message['Subject'] = subject

    # Add the message body
    email_message.attach(MIMEText(message, 'plain'))

    # SMTP server configuration
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = sender_email
    smtp_password = os.environ["password"]

    # Create a secure connection with the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(email_message)

    print('Email sent successfully')

if __name__ == "__main__":
        main()