provider "google" {
  project = "marine-bison-360321"
  region  = "us-east1"
  zone    = "us-east1-b"
}

resource "google_storage_bucket" "datalake" {
  name          = "reddit-posts3"
  force_destroy = false
  location      = "US-EAST1"
  storage_class = "STANDARD"
  versioning {
    enabled = false 
  }
}

resource "google_storage_bucket_object" "picture" {
  name   = "stop_words.txt"
  source = "stop_words.txt"
  bucket = google_storage_bucket.datalake.name
  depends_on = [google_storage_bucket.datalake]
}


resource "google_bigquery_dataset" "dataset" {
  dataset_id                  = "reddit_words2"
  description                 = "Data warehouse"
  location                    = "US-EAST1"

}
