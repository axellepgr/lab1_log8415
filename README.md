# Cluster Benchmarking using EC2 Virtual Machines and Elastic Load Balancer (ELB)

## Instructions

To reproduce the experiment, all you have to do is download the main.sh file and run it on your local computer. Make sure you have an internet connection and an AWS account

## Description

This project creates 5 m4.large and 4 t2.large EC2 instances in your AWS account, deploys a simple flask app on the EC2 instances, sets up a VPC and a load balancer that is connected to the EC2 instances, sends 2500 GET requests to the load balancer and retreives ClouWatch metrics and puts them in a .json file inside the /src directory and displays the metrics as graphs.

While running the main.sh bash script, you will be prompted to:

1. Set up your AWS credentials file (~/.aws/credentials).
2. Put your SSH key (.pem file) inside the /src folder after clonning the repository.
