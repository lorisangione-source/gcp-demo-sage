resource "google_firestore_database" "sage" {
  project     = var.project_id
  name        = local.firestore_db
  location_id = var.region
  type        = "FIRESTORE_NATIVE"
}

resource "google_firestore_index" "chunks_embedding" {
  project    = var.project_id
  database   = google_firestore_database.sage.name
  collection = "chunks"

  fields {
    field_path = "embedding"
    vector_config {
      dimension = 768
      flat {}
    }
  }
}
