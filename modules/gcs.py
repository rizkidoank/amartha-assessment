from google.cloud import storage
import click

class GcsScanner(object):
    def __init__(self, project_id):
        self.storage_client = storage.Client(project=project_id)
        self.project_id = project_id

    def isPublicBucket(self, bucket):
        for policy in bucket.get_iam_policy().bindings:
            members = policy["members"]
            if ("allUsers" in members) or ("allAuthenticatedUsers" in members):
                return True

    def scanner_list_buckets(self):
        buckets = self.storage_client.list_buckets()
        return buckets

    def scanner_list_public_bucket(self):
        buckets = self.scanner_list_buckets()
        public_buckets = []
        for bucket in buckets:
            if self.isPublicBucket(bucket):
                public_buckets.append(bucket.name)
        
        return public_buckets

    def scanner_list_public_objects(self, bucket_name):
        bucket = self.storage_client.get_bucket(bucket_name)
        public_objects = []

        click.echo("Populate and counting the public objects in {}".format(bucket_name))
        # all objects in public bucket are public
        if self.isPublicBucket(bucket):
            for blob in bucket.list_blobs():
                public_objects.append(blob.name)
        # if its not public, look over the blob acl
        else:
            for blob in bucket.list_blobs():
                for acl in blob.acl:
                    if ("allUsers" == acl["entity"]) or ("allAuthenticatedUsers" == acl["entity"]):
                        public_objects.append(blob.name)
                        
        return public_objects
