provider "google" {
  project = "your-project-id"
  region  = "us-central1"
}

resource "google_storage_bucket" "trigger_bucket" {
  name     = "exercicio2-uploads-${uuid().result}"
  location = "US"
}

resource "google_storage_bucket" "code_bucket" {
  name     = "exercicio2-code-${uuid().result}"
  location = "US"
}

resource "google_storage_bucket_object" "archive" {
  name   = "index.zip"
  bucket = google_storage_bucket.code_bucket.name
  source = "./function-source.zip"
}

resource "google_cloudfunctions_function" "function" {
  name        = "exercicio2-function"
  runtime     = "python39"

  source_archive_bucket = google_storage_bucket.code_bucket.name
  source_archive_object = google_storage_bucket_object.archive.name
  entry_point           = "process_s3_event"

  event_trigger {
    event_type = "google.storage.object.finalize"
    resource   = google_storage_bucket.trigger_bucket.name
  }
}
