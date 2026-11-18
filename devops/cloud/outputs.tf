output "cloud_run_url" {
  value = google_cloud_run_v2_service.sage.uri
}

output "instructions_bucket" {
  value = google_storage_bucket.instructions.name
}
