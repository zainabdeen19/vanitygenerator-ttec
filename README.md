# Setting up and Deploying Vanity Phone Number Generator Service on AWS using Terraform and AWS CLI

## Introduction
This guide provides instructions on setting up and deploying the Vanity Phone Number Generator Service on AWS using Terraform and AWS CLI. The Vanity Phone Number Generator Service is a straightforward application designed to generate unique vanity phone numbers based on the user's input.

## Prerequisites
To successfully follow these instructions, ensure that the following prerequisites are installed on your system:
- Git
- Terraform CLI
- AWS CLI

## Steps to Set up and Deploy the Vanity Phone Number Generator Service

### 1. Clone the repository
Clone the repository using the following command:

git clone https://github.com/zainabdeen19/vanitygenerator-ttec


### 2. Set up AWS CLI
Configure the AWS CLI by running the following command and providing the necessary information:

aws configure


### 3. Set up Terraform CLI
Download and install the Terraform CLI from the official website: [Terraform Downloads](https://www.terraform.io/downloads.html)

### 4. Initialize Terraform
Open a terminal in the root folder of the cloned repository and run the following command to initialize Terraform:

terraform init

This command downloads the necessary provider plugins and initializes Terraform for the project. It may take up to 2 minutes to complete.

### 5. Plan the infrastructure (Optional)
Run the following command to preview the infrastructure changes that Terraform will make:

terraform plan

### 6. Deploy the infrastructure
Run the following command to deploy the infrastructure to AWS:

terraform apply -auto-approve

This command creates all the necessary resources on AWS, including an Amazon Connect instance, an Amazon S3 bucket, and an Amazon CloudFront distribution. It may take up to 5 minutes to complete.

### KNOWN ISSUES
This command might generate an error “Error creating connect queue (dataqueue)”. You can ignore this error as it's a known issue with the AWS API for creating the queue. There might also be some warnings, which can be ignored.

### 7. Setup Connect Instance
1. Go to the Amazon Connect console and click on "Contact Flows."
2. Click on the Instance name with the prefix "VanityGenerator."
3. Now, you can see instance settings; click on Emergency Access.
4. Once logged in, select your phone number and follow the steps to configure the contact flow.

**Note:** When calling the service for the first time, it may not generate numbers initially as the app initializes the database. It should work on the second call.```

# BONUS TASK

I was more comfortable with using Terraform for IaaC and with Terraform AWS has revised their policies for S3 bucket due to which I cannot disable ACLs directly using Terraform script. Due to this reason all objects are private and I would have to make them public manually which defeats the purpose of using Terraform. I still have uploaded the react code for the front end web app in the repo and it is being delpoyed in the S3 bucket as well but due to some permission issues it is private.
