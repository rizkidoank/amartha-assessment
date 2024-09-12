from .gcs import GcsScanner
from .config import Config

from fpdf import FPDF
from smtplib import SMTP_SSL
from email.message import EmailMessage

import click
import ssl

class Utils(object):
    def __init__(self, project_id):
        self.project_id = project_id

    def render_report_gcs(self):
        scanner = GcsScanner(self.project_id)
        click.echo("Scan the public buckets in {} project...".format(self.project_id))

        public_buckets = scanner.scanner_list_public_bucket()
        public_objects = {}
        buckets = scanner.scanner_list_buckets()
        for bucket in buckets:
            click.echo("Scan the public objects in bucket {}...".format(bucket))
            public_objects[bucket.name] = scanner.scanner_list_public_objects(bucket.name)

        click.echo("Composing PDF for the report summary...")
        pdf = FPDF()

        # print public buckets page
        pdf.add_page()
        pdf.set_font("helvetica", size=12)
        pdf.write(text="Project ID: {}".format(self.project_id), h=10)
        pdf.ln()
        pdf.write(text="Below are public buckets in the given project:", h=10)
        pdf.ln()
        data = [[bucket] for bucket in public_buckets]
        data.insert(0, ["Bucket Name"])
        with pdf.table() as table:
            for data_row in data:
                table.row(data_row)

        # print public objects page for each bucket if exists
        for bucket, objects in public_objects.items():
            if len(objects) > 0:
                pdf.add_page()
                pdf.set_font("helvetica", size=12)
                pdf.write(text="Project ID: {}".format(self.project_id), h=10)
                pdf.ln()
                pdf.write(text="Bucket Name: {}".format(bucket), h=10)
                pdf.ln()
                pdf.write(text="Total Public Objects: {}".format(len(objects)), h=10)
                pdf.ln()
                pdf.write(text="Below are public objects in the given bucket:", h=10)
                pdf.ln()
                data = [[object] for object in objects]
                data.insert(0, ["Object Name"])
                with pdf.table() as table:
                    for data_row in data:
                        table.row(data_row)

        click.echo("Export the PDF to local...")
        pdf.output("report.pdf")
        return "report.pdf"
    
    def send_email_smtp(self, smtp_server, smtp_username, smtp_password, smtp_sender, target_email, attachment):        
        context = ssl.create_default_context()
        try:
            with SMTP_SSL(smtp_server, 465, context) as server:
                click.echo("Login to SMTP server...")
                server.login(smtp_username, smtp_password)
                click.echo("composing the email...")
                message = EmailMessage()
                message['Subject'] = "Report GCS Public Buckets and Objects"
                message['From'] = smtp_sender
                message['To'] = target_email
                message.set_content("Please find the report summary for GCS scanning results in attached document.")
                with open(attachment,'rb') as f:
                    content = f.read()
                    message.add_attachment(content, maintype='application', subtype='pdf', filename=attachment)
                click.echo("Sending email...")
                server.send_message(message)
                server.quit()
                click.echo("Email sent, closing the SMTP connection...")
        except Exception as e:
            click.echo(e)