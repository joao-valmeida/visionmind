provider "google" {
  project = "your-project-id"
  region  = "us-central1"
}

resource "google_compute_network" "vpc" {
  name = "exercicio3-vpc"
}

resource "google_vpc_access_connector" "connector" {
  name          = "ex3-connector"
  network       = google_compute_network.vpc.name
  ip_cidr_range = "10.8.0.0/28"
  region        = "us-central1"
}

resource "google_pubsub_topic" "topic" {
  name = "exercicio3-topic"
}

resource "google_sql_database_instance" "postgres" {
  name             = "exercicio3-db"
  region           = "us-central1"
  database_version = "POSTGRES_14"
  settings {
    tier = "db-f1-micro"
    ip_configuration {
      ipv4_enabled    = false
      private_network = google_compute_network.vpc.id
    }
  }
}

resource "google_cloudfunctions_function" "function" {
  name        = "exercicio3-function"
  runtime     = "python39"
  entry_point = "process_queue"

  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource   = google_pubsub_topic.topic.name
  }

  vpc_connector = google_vpc_access_connector.connector.name
  
  environment_variables = {
    DB_HOST = google_sql_database_instance.postgres.private_ip_address
    DB_NAME = "postgres"
    DB_USER = "postgres"
    DB_PASS = "mypassword"
  }
}
