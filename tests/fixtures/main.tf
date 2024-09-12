terraform {
  required_providers {
    google = {
      source  = "opentofu/google"
      version = "6.0.0"
    }
  }
}

locals {
  project_id                                            = "papaops-develop"
  public_bucket_public_objects_count                    = 11
  default_bucket_public_objects_count                   = 6
  default_bucket_objects_count                          = 6
  uniform_bucket_public_objects_count                   = 9
  uniform_all_authenticated_bucket_public_objects_count = 12
}

provider "google" {

}

resource "random_id" "enforced_bucket" {
  byte_length = 4
}

resource "random_id" "public" {
  byte_length = 4
}

resource "random_id" "default" {
  byte_length = 4
}

resource "random_id" "uniform" {
  byte_length = 4
}

resource "google_storage_bucket" "enforced" {
  project       = local.project_id
  name          = "enforced-${random_id.enforced_bucket.hex}"
  location      = "ASIA"
  force_destroy = true

  public_access_prevention = "enforced"
}


resource "google_storage_bucket_iam_member" "all_users" {
  bucket = google_storage_bucket.public.name
  role   = "roles/storage.objectViewer"
  member = "allUsers"
}

resource "google_storage_bucket" "public" {
  project       = local.project_id
  name          = "public-${random_id.enforced_bucket.hex}"
  location      = "ASIA"
  force_destroy = true
}

resource "google_storage_bucket" "default" {
  project       = local.project_id
  name          = "default-${random_id.default.hex}"
  location      = "ASIA"
  force_destroy = true
}

resource "google_storage_bucket" "uniform" {
  project                     = local.project_id
  name                        = "uniform-${random_id.enforced_bucket.hex}"
  location                    = "ASIA"
  force_destroy               = true
  uniform_bucket_level_access = true
}

resource "google_storage_bucket" "uniform_all_authenticated" {
  project                     = local.project_id
  name                        = "uniform-all-authenticated-${random_id.enforced_bucket.hex}"
  location                    = "ASIA"
  force_destroy               = true
  uniform_bucket_level_access = true
}

resource "google_storage_bucket_iam_member" "all_authenticated_users" {
  bucket = google_storage_bucket.uniform_all_authenticated.name
  role   = "roles/storage.objectViewer"
  member = "allAuthenticatedUsers"
}

resource "google_storage_bucket_object" "public" {
  count  = local.public_bucket_public_objects_count
  name   = "/sad/public-object-${count.index}"
  bucket = google_storage_bucket.public.name
  source = "aiyodummy.txt"
}

resource "google_storage_bucket_object" "default_public" {
  count  = local.default_bucket_public_objects_count
  name   = "public-object-${count.index}"
  bucket = google_storage_bucket.default.name
  source = "aiyodummy.txt"
}

resource "google_storage_object_access_control" "default_public" {
  count =  local.default_bucket_public_objects_count
  object = google_storage_bucket_object.default_public[count.index].output_name
  bucket = google_storage_bucket.default.name
  role   = "READER"
  entity = "allUsers"
}

resource "google_storage_bucket_object" "default" {
  count  = local.default_bucket_objects_count
  name   = "object-${count.index}"
  bucket = google_storage_bucket.default.name
  source = "aiyodummy.txt"
}