provider "google" {
  project = var.project_id
  region  = var.region
}

variable "region" {
  description = "GCP region used by exercise 1 resources."
  type        = string
  default     = "us-central1"
}

variable "bucket_location" {
  description = "GCS bucket location used to store Cloud Function source."
  type        = string
  default     = "US"
}

variable "resource_prefix" {
  description = "Prefix for exercise 1 resource names."
  type        = string
  default     = "exercicio1"
}

resource "google_project_service" "firestore" {
  project            = var.project_id
  service            = "firestore.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "cloudfunctions" {
  project            = var.project_id
  service            = "cloudfunctions.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "cloudbuild" {
  project            = var.project_id
  service            = "cloudbuild.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "iam" {
  project            = var.project_id
  service            = "iam.googleapis.com"
  disable_on_destroy = false
}

resource "google_service_account" "function" {
  project      = var.project_id
  account_id   = "${var.resource_prefix}-function-sa"
  display_name = "Exercise 1 Cloud Function service account"

  depends_on = [google_project_service.iam]
}

resource "google_project_iam_member" "function_datastore_user" {
  project = var.project_id
  role    = "roles/datastore.user"
  member  = "serviceAccount:${google_service_account.function.email}"
}

resource "random_id" "bucket_suffix" {
  byte_length = 4
}

data "archive_file" "function_source" {
  type        = "zip"
  output_path = "${path.module}/function-source.zip"

  source {
    content  = file("${path.module}/main.py")
    filename = "main.py"
  }

  source {
    content  = file("${path.module}/requirements.txt")
    filename = "requirements.txt"
  }
}

resource "google_storage_bucket" "bucket" {
  name     = "${var.resource_prefix}-bucket-${random_id.bucket_suffix.hex}"
  location = var.bucket_location
}

resource "google_storage_bucket_object" "archive" {
  name   = "index-${data.archive_file.function_source.output_md5}.zip"
  bucket = google_storage_bucket.bucket.name
  source = data.archive_file.function_source.output_path
}

resource "google_cloudfunctions_function" "function" {
  name        = "${var.resource_prefix}-function"
  description = "Exercise 1 Function"
  runtime     = "python312"

  available_memory_mb   = 256
  source_archive_bucket = google_storage_bucket.bucket.name
  source_archive_object = google_storage_bucket_object.archive.name
  service_account_email = google_service_account.function.email
  trigger_http          = true
  entry_point           = "handle_items"

  depends_on = [
    google_project_service.cloudbuild,
    google_project_service.cloudfunctions,
    google_project_service.firestore,
    google_project_iam_member.function_datastore_user,
  ]
}

# IAM entry for all users to invoke the function (for educational purposes)
resource "google_cloudfunctions_function_iam_member" "invoker" {
  project        = google_cloudfunctions_function.function.project
  region         = google_cloudfunctions_function.function.region
  cloud_function = google_cloudfunctions_function.function.name

  role   = "roles/cloudfunctions.invoker"
  member = "allUsers"
}

resource "google_firestore_database" "database" {
  project     = var.project_id
  name        = "(default)"
  location_id = var.region
  type        = "FIRESTORE_NATIVE"

  depends_on = [google_project_service.firestore]
}

output "function_url" {
  description = "HTTP endpoint URL for the items API"
  value       = google_cloudfunctions_function.function.https_trigger_url
}
