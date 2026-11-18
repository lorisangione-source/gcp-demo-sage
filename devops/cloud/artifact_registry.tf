resource "google_artifact_registry_repository" "sage" {
  location      = var.region
  repository_id = local.app_name
  description   = "Immagini Docker per ${local.app_name}"
  format        = "DOCKER"
}
