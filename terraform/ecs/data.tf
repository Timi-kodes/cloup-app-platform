data "aws_vpc" "main" {
  filter {
    name   = "tag:Name"
    values = ["cloud-app-vpc"]
  }
}

data "aws_subnets" "public" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.main.id]
  }

  filter {
    name   = "tag:Name"
    values = ["public-*"]
  }
}
