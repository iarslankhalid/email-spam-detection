import os
from bs4 import BeautifulSoup
import re
import email

class ParsedEmail:
    def __init__(self, raw_email, filename, label=None):
        self.raw_email = raw_email
        self.email_message = None
        self.filename = filename
        self.Date = None
        self.From = None
        self.To = None
        self.Subject = None
        self.Body = None
        self.Label = label
        self._parse_email()

    def _parse_email(self):
        # Parse the email message
        self.email_message = email.message_from_string(self.raw_email)

        # Extract headers
        self.Date = self.email_message.get('Date')
        self.From = self.email_message.get('From')
        self.To = self.email_message.get('To')
        self.Subject = self.email_message.get('Subject')

        # Extract and clean the body
        self.Body = self._get_clean_body()

    def _get_clean_body(self):
        body = ""

        # If the message is multipart, we need to extract the actual body part
        if self.email_message.is_multipart():
            for part in self.email_message.walk():
                # Try to extract plain text first
                if part.get_content_type() == 'text/plain':
                    body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    break
                # If HTML content is found, clean it up
                elif part.get_content_type() == 'text/html':
                    html_content = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    body = self._clean_html(html_content)
                    break
        else:
            # Handle single-part emails
            if self.email_message.get_content_type() == 'text/plain':
                body = self.email_message.get_payload(decode=True).decode('utf-8', errors='ignore')
            elif self.email_message.get_content_type() == 'text/html':
                html_content = self.email_message.get_payload(decode=True).decode('utf-8', errors='ignore')
                body = self._clean_html(html_content)

        # Clean the body (apply the same cleaning process from earlier)
        body = re.sub(r'^\s*>.*$', '', body, flags=re.MULTILINE)  # Remove quoted text
        body = re.sub(r'https?://\S+', '', body)  # Remove URLs
        body = re.split(r'\n--\n', body)[0]  # Remove signature block
        body = re.sub(r'\s+', ' ', body).strip()  # Normalize whitespace
        return body

    @staticmethod
    def _clean_html(html_content):
        """Removes HTML tags from content using BeautifulSoup"""
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.get_text(separator=' ')


def read_emails_from_folder(folder_path, label):
    folder_emails = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'rb') as file:
            try:
                raw_email = file.read().decode('utf-8', errors='ignore')
                parsed_email = ParsedEmail(raw_email, filename, label)
                folder_emails.append(parsed_email)
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    return folder_emails