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
        enabled = false
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