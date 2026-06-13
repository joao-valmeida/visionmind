provider "google" {
  project = "your-project-id"
  region  = "us-central1"
}

resource "google_storage_bucket" "bucket" {
  name     = "exercicio1-bucket-${uuid().result}"
  location = "US"
}

resource "google_storage_bucket_object" "archive" {
  name   = "index.zip"
  bucket = google_storage_bucket.bucket.name
  source = "./function-source.zip" # Students should zip main.py and requirements.txt
}

resource "google_cloudfunctions_function" "function" {
  name        = "exercicio1-function"
  description = "Exercise 1 Function"
  runtime     = "python39"

  available_memory_mb   = 256
  source_archive_bucket = google_storage_bucket.bucket.name
  source_archive_object = google_storage_bucket_object.archive.name
  trigger_http          = true
  entry_point           = "handle_items"
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
  project     = "your-project-id"
  name        = "(default)"
  location_id = "us-central1"
  type        = "FIRESTORE_NATIVE"
}
