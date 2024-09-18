# AWS emulation with Localstack, Terraform and Boto3

This repository contains a series of experiments and proof-of-concepts (PoC) for using Localstack, Terraform and boto3 to emulate AWS services in local environment. The goal of these projects is to explore, test and optimize the interaction between infrastructure defined through Terraform, AWS resources (such as S3, DynamoDB, Lambda) and Python.

## Technologies used ⚙️

* **Localstack**:  a local platform for AWS development
* **Docker compose**: for defining and running multi-container applications
* **Terraform**: an Infrastructure as a Code tool for managing AWS resources
* **Boto3**: a Python SDK for AWS

## Objectives 🎯

* Simulate a cloud environment locally
* Perform tests without incurring costs on real cloud resource
* Automate infrastructure creation with IaaC tools
