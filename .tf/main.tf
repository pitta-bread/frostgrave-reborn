terraform {
    required_providers {
        google = {
            source  = "hashicorp/google"
            version = "~> 6.0"
        }
    }
}

provider "google" {
    project = "frostgrave-reborn"
    region  = "europe-west2"
}

data "google_client_openid_userinfo" "me" {}

data "google_client_config" "current" {}

resource "google_storage_bucket" "frostgrave_bucket" {
    name          = "frostgrave-reborn-private"
    location      = "EU"
    force_destroy = false
    versioning {
        enabled = true
    }

    # delete versions older than 7 days, not objects
    lifecycle_rule {
        action {
            type = "Delete"
        }
        condition {
            age = 7
            with_state = "ARCHIVED"
        }
    }

    uniform_bucket_level_access = true
}

resource "google_artifact_registry_repository" "docker_repo" {
    repository_id = "frostgrave-reborn"
    description   = "Docker images for frostgrave-reborn"
    format        = "DOCKER"
}

output "registry_location" {
    description = "The location of the Docker registry"
    value       = "${google_artifact_registry_repository.docker_repo.location}-docker.pkg.dev/${google_artifact_registry_repository.docker_repo.project}/${google_artifact_registry_repository.docker_repo.repository_id}"
}

resource "google_cloud_run_v2_service" "frostgrave_service" {
    name        = "frostgrave-reborn"
    location    = "europe-west2"

    ingress     = "INGRESS_TRAFFIC_ALL"

    invoker_iam_disabled = true

    template {
        execution_environment   = "EXECUTION_ENVIRONMENT_GEN2"
        service_account         = "13426297955-compute@developer.gserviceaccount.com"
        session_affinity        = true
        timeout                 = "60s"

        scaling {
            max_instance_count = 1
        }

        volumes {
            name = "gcs-1"
            gcs {
                bucket    = "frostgrave-reborn-private"
                read_only = false # Assuming read-write access is needed.
            }
        }

        containers {
            image = "${google_artifact_registry_repository.docker_repo.location}-docker.pkg.dev/${google_artifact_registry_repository.docker_repo.project}/${google_artifact_registry_repository.docker_repo.repository_id}/image:latest"
            
            resources {
                limits = {
                    cpu    = "1"
                    memory = "1Gi"
                }
                startup_cpu_boost = true
            }

            ports {
                container_port = 8000
                name           = "http1"
            }

            startup_probe {
                timeout_seconds   = 240
                period_seconds    = 240
                failure_threshold = 1
                tcp_socket {
                    port = 8000
                }
            }

            volume_mounts {
                name       = "gcs-1"
                mount_path = "/mnt/gcs_frostgrave_reborn"
            }
        }
    }

    traffic {
        type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
        percent = 100
  }
}

output "service_url" {
    description = "The URL of the deployed Cloud Run service."
    value       = google_cloud_run_v2_service.frostgrave_service.uri
}

output "service_name" {
    description = "The name of the Cloud Run service."
    value       = google_cloud_run_v2_service.frostgrave_service.name
}