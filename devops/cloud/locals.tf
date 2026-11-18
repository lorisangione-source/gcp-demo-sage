locals {
  has_prefix               = var.resource_prefix != ""
  app_name                 = local.has_prefix ? "${var.resource_prefix}-sage" : "sage"
  firestore_db             = local.has_prefix ? var.resource_prefix : "(default)"
  docs_bucket_name         = local.has_prefix ? "${var.resource_prefix}-sage-docs" : "${var.project_id}-sage-docs"
  instructions_bucket_name = local.has_prefix ? "${var.resource_prefix}-instructions" : "${var.project_id}-instructions"

  raw_sa_id = "${local.app_name}-run"
  sa_id     = length(local.raw_sa_id) <= 30 ? local.raw_sa_id : "${substr(local.raw_sa_id, 0, 23)}-${substr(sha256(local.raw_sa_id), 0, 6)}"
}
