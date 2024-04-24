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
        self.places_mail_sent_10 = []
        
        # time items
        self.start_time = time.monotonic()
        self.last_run_time = 0
        self.current_time = 0
        self.elapsed_time = 0
        self.record_time()
        
    def record_time(self):
        self.current_time = time.monotonic()
        self.elapsed_time = self.current_time - self.start_time
    
    def reset_places_sent(self):
        if (self.elapsed_time - self.last_run_time) > 600:
            self.places_mail_sent_10 = []
            self.last_run_time = self.elapsed_time

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
        place_not_to_match = "Coteau-du-Lac, QC Canada"
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
    
    def add_mail_sent(self, places):
        for place in places:
            if place not in self.places_mail_sent_10:
                self.places_mail_sent_10.append(place)
    
    def check_mail_sent(self, places):
        if places == []:
            return False
        for place in places:
            if place not in self.places_mail_sent_10:
                return True
        return False
        
    
    def send_email(self):
        places_QC, places_BC, QC, BC = self.check_places()
        
        self.record_time()
        
        check_mail_QC = self.check_mail_sent(places_QC)
        check_mail_BC = self.check_mail_sent(places_BC)
        
        if self.email:
            email_sender = EmailSender(self.sender_email, self.sender_password)
            log_msg = ""
            if QC and check_mail_QC:
                log_msg += email_sender.send_email(places_QC, "QC")
                self.add_mail_sent(places_QC)
            if BC and check_mail_BC:
                log_msg += email_sender.send_email(places_BC, "BC")
                self.add_mail_sent(places_BC)
            if not log_msg == "":
                self.logger.info(log_msg)      
        
        self.reset_places_sent()