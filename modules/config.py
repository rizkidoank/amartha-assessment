from pathlib import Path
import configparser
import click

class Config(object):
    def __init__(self):
        self.config_file = Path("{}/.scanner/config.ini".format(Path.home()))

    def build_config(self):
        config = configparser.ConfigParser()
        smtp_server = click.prompt("Enter your SMTP server, only support SSL", type=str)
        smtp_user = click.prompt("Enter your SMTP user", type=str)
        smtp_pass = click.prompt("Enter your SMTP password", type=str, hide_input=True)
        smtp_sender = click.prompt("Enter your SMTP sender", type=str)
        config['SMTP'] = {
            'smtp_server': smtp_server,
            'smtp_user': smtp_user,
            'smtp_password': smtp_pass,
            'smtp_sender': smtp_sender
        }

        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with self.config_file.open('w', encoding="utf-8") as f:
            config.write(f)


    def check_config(self):
        generate_config_confirmation = False
        try:
            self.config_file.resolve(strict=True)
            generate_config_confirmation = click.confirm("Config exists, do you want to generate again?", abort=True)
        except FileNotFoundError as e:
            click.echo(e, err=True)
            generate_config_confirmation = click.confirm("Build new config?", abort=True)
        if generate_config_confirmation:
            self.build_config()
    
    def read_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_file)
        return config