# -*- coding: utf-8 -*-
import click
import logging
import os
import csv

from parse_email import read_emails_from_folder


@click.command()
@click.argument('input_directory', default = 'data/raw', type=click.Path(exists=True))
@click.argument('output_directory', default = 'data/interim', type=click.Path())
def main(input_directory, output_directory):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info(f'Loading raw data from {input_directory}')

    # Paths for different email categories
    easy_ham_path = os.path.join(input_directory, 'easy_ham')
    hard_ham_path = os.path.join(input_directory, 'hard_ham')
    spam_path = os.path.join(input_directory, 'spam_2')

    logger.info(f"Parsing & Labeling the data from {easy_ham_path}, {hard_ham_path}, {spam_path}")

    # Read and label emails
    easy_ham_parsed_emails = read_emails_from_folder(easy_ham_path, label=0)
    hard_ham_parsed_emails = read_emails_from_folder(hard_ham_path, label=0)
    spam_parsed_emails = read_emails_from_folder(spam_path, label=1)

    logger.info(f"Creating and saving csv file in '{output_directory}' for parsed emails")

    # Combine all parsed emails
    parsed_emails = easy_ham_parsed_emails + hard_ham_parsed_emails + spam_parsed_emails

    # Specify the output CSV file name
    output_csv_path = os.path.join(output_directory, 'parsed_emails.csv')
    create_csv_from_parsed_emails(parsed_emails, output_csv_path)


def create_csv_from_parsed_emails(parsed_emails, output_csv_path):
    """ Writes parsed emails to a CSV file. """
    headers = ['Filename', 'Date', 'From', 'To', 'Subject', 'Body', 'Label']

    with open(output_csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()

        for email in parsed_emails:
            writer.writerow({
                'Filename': email.filename,
                'Date': email.Date,
                'From': email.From,
                'To': email.To,
                'Subject': email.Subject,
                'Body': email.Body,
                'Label': email.Label
            })


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # Click command handles the arguments
    main()