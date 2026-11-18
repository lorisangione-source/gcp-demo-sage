resource "google_cloud_run_v2_service" "sage" {
  name                = local.app_name
  location            = var.region
  deletion_protection = false

  template {
    service_account = google_service_account.sage_run.email

    containers {
      image = "us-docker.pkg.dev/cloudrun/container/hello"

      env {
        name  = "SAGE_PROJECT_ID"
        value = var.project_id
      }
      env {
        name  = "SAGE_REGION"
        value = var.region
      }
      env {
        name  = "SAGE_RESOURCE_PREFIX"
        value = var.resource_prefix
      }
      env {
        name  = "SAGE_INSTRUCTIONS_BUCKET"
        value = google_storage_bucket.instructions.name
      }
    }
  }

  lifecycle {
    ignore_changes = [
      template[0].containers[0].image,
      client,
      client_version,
    ]
  }
}

resource "google_cloud_run_v2_service_iam_member" "public_invoker" {
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.sage.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
