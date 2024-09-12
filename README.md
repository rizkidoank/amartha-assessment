## GCS Scanner
This is a CLI tool to scan public bucket and public objects in a bucket within a project ID. Its also has capability to send report summary to email using SMTP SSL.

### Features
- List Public Bucket
    - command: `scanner gcs list-public-bucket --project-id PROJECT_ID`
- List Public Objects
    - command: `scanner gcs list-public-objects BUCKET_NAME --project-id PROJECT_ID`
- Send Summary
    - command: `scanner gcs send-summary --target-email 'TARGET_EMAIL' --project-id PROJECT_ID`

### How to Install
#### Requirements
- Python 3.12
- `poetry`
    - install with `pip install poetry`
- SMTP SSL account
- GCP JSON credentials
    - use `export GOOGLE_APPLICATION_CREDENTIALS=PATH_TO_JSON_KEY`

#### Installation Steps
1. Ensure you already has `python` and `poetry` installed
2. Run `poetry install`
3. To run the command, you may run `poetry run scanner COMMANDS`

### Configuration Attributes
The configuration stored in `.ini` at `$HOME/.scanner/config.ini`. The sample config is as follows:
```
[SMTP]
smtp_server = SMTP_SERVER
smtp_user = SMTP_USER
smtp_password = SMTP_PASS
smtp_sender = SMTP_SENDER
```
This config can be generated with `Send Summary` command if its not exists.

### Additional Informations
- For testing, the tests fixture provided at `tests/fixtures`
    - You need to use `opentofu` to create the buckets and objects

#### Creating Tests Fixture
1. Ensure you have `opentofu`
2. Export the Google Credentials with `export GOOGLE_CREDENTIALS=PATH_TO_JSON`
3. Run `tofu init`
4. Run `tofu plan`, review the changes
5. Run `tofu apply` to make the fixtures
6. Destroy the resources with `tofu destroy`
