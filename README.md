# Custom Ubuntu AMI Creation Script

This repository contains a Python script that automates the process of creating a custom Amazon Machine Image (AMI) with pre-installed software on an Ubuntu EC2 instance. The script uses Boto3, the AWS SDK for Python, to handle the automation.

## Features

- Launches an EC2 instance with Ubuntu 20.04 LTS.
- Installs and configures the following software:
  - NGINX
  - Git
  - Python3 and pip
  - NPM
  - Docker
- Creates an AMI from the customized instance.
- Terminates the EC2 instance after the AMI is created.

## Prerequisites

- Python 3.x
- Boto3
- AWS credentials configured on your local machine (`~/.aws/credentials` or environment variables).

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/jasontt33/automated-ami-build.git
   cd custom-ubuntu-ami
