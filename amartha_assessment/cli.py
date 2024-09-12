from modules.config import Config
from modules.gcs import GcsScanner
from modules.utils import Utils

import click

@click.group
def cli():
    pass

@click.group()
def gcs():
    pass

@click.command()
@click.option('--project-id', help="GCP project to scan", required=True)
def list_public_bucket(project_id):
    scanner = GcsScanner(project_id)
    public_buckets = scanner.scanner_list_public_bucket()
    for bucket in public_buckets:
        click.echo(bucket)

@click.command()
@click.option('--project-id', help="GCP project to scan", required=True)
@click.argument('bucket-name')
def list_public_objects(project_id, bucket_name):
    scanner = GcsScanner(project_id)
    public_objects = scanner.scanner_list_public_objects(bucket_name)
    for object in public_objects:
        click.echo(object)

@click.command()
@click.option('--project-id', help="GCP project to scan", required=True)
@click.option('--target-email', help="email to send the summary", required=True)
def send_summary(project_id, target_email):
    config = Config()
    utils = Utils(project_id)
    try:
        report = utils.render_report_gcs()
        smtp_server = config.read_config().get('SMTP', 'smtp_server')
        smtp_user = config.read_config().get('SMTP', 'smtp_user')
        smtp_password = config.read_config().get('SMTP', 'smtp_password')
        smtp_sender = config.read_config().get('SMTP', 'smtp_sender')
        utils.send_email_smtp(smtp_server, smtp_user, smtp_password, smtp_sender, target_email, report)
    except Exception as e:
        click.echo(e, err=True)
        config.check_config()
        click.echo("please rerun the tools again")


cli.add_command(gcs)
gcs.add_command(list_public_bucket)
gcs.add_command(list_public_objects)
gcs.add_command(send_summary)

if __name__=="__main__":
    cli()
