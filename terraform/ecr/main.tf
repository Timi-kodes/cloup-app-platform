terraform {
  backend "s3" {
    bucket         = "cloud-app-platform-tf-state"
    key            = "ecr/terraform.tfstate"
    region         = "eu-north-1"
    dynamodb_table = "terraform-locks"
  }
}

provider "aws" {
  region = "eu-north-1"
}


resource "aws_ecr_repository" "app" {
  name = "cloud-app-platform"
  image_scanning_configuration {
    scan_on_push = true
  }
}
