resource "google_storage_bucket" "docs" {
  name                        = local.docs_bucket_name
  location                    = var.region
  uniform_bucket_level_access = true
  force_destroy               = true
}

resource "google_storage_bucket" "instructions" {
  name                        = local.instructions_bucket_name
  location                    = var.region
  uniform_bucket_level_access = true
  force_destroy               = true
}
