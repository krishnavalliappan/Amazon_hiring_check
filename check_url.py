import time
import requests
from bs4 import BeautifulSoup
from send_mail import EmailSender

class CheckURL:
    def __init__(self, url, logger, sender_email, sender_password):
        self.url = url
        self.logger = logger
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.QC_text = "QC Canada"
        self.BC_text = "BC Canada"
        self.email = False
        
    def fetch_data(self):
        response = requests.get(self.url)
        # check the response
        if response.status_code != 200:
            self.logger.exception(f"Exception occured during fetching URL, response code: {response.status_code}")
            return None
        else:
            # Now you use Beautiful Soup to parse the response text
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup

    def find_all_places(self, soup):
        if not soup:
            return []
        # Find all 'div' elements with class 'listing row'
        listing_rows = soup.find_all('div', class_='listing row')
    
        # Find all 'h6' elements that are descendants of something other than 'div.listing row'
        # Then find all 'span' elements within those 'h6' elements
        spans = []
        # spans are the list of places.
        for listing_row in listing_rows:
            # We find all 'h6' that are not direct children of the 'listing_row'
            h6s = listing_row.find_all('h6')
            for h6 in h6s:
                # Now we check if 'span' is inside 'h6'
                spans_inside_h6 = h6.find_all('span')
                spans.extend(spans_inside_h6)
        return spans
    
    def place_match(self, place, place_to_match):
        place_not_to_match = "Coteau-du, QC Canada"
        if place[-9:] == place_to_match:
            if place == place_not_to_match:
                return False
            return True
    
    def check_places(self):
        
        all_places = self.find_all_places(self.fetch_data())
        
        QC = False
        BC = False
        places_QC = []
        places_BC = []
        
        if not all_places:
            return [], [], False, False
        
        for place in all_places:
            if self.place_match(place.text, self.QC_text):
                QC = True
                places_QC.append(place.text)
                break
            elif self.place_match(place.text, self.BC_text):
                BC = True
                places_BC.append(place.text)
                break
        
        if QC or BC:
            self.email = True
            return places_QC, places_BC, QC, BC
        else:
            return [], [], False, False
    
    def send_email(self):
        places_QC, places_BC, QC, BC = self.check_places()

        
        if self.email:
            email_sender = EmailSender(self.sender_email, self.sender_password)
            log_msg = ""
            if QC:
                log_msg += email_sender.send_email(places_QC, "QC")
            if BC:
                log_msg += email_sender.send_email(places_BC, "BC")
            self.logger.info(log_msg)
            
        else:
            self.logger.info("No email sent")
