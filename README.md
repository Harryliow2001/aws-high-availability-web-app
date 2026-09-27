# Highly Available Web Application on AWS

A hands-on AWS cloud and DevOps project demonstrating high availability, fault tolerance, elastic scaling, private networking, monitoring, secure AWS service access, and automated CI/CD deployment using GitHub Actions.
The application runs on private EC2 instances across multiple Availability Zones behind an Application Load Balancer and is managed by an Auto Scaling Group.


## Architecture
![Uploading architecture diagram.png…]()

## AWS Services Used
- Amazon VPC
- Amazon EC2
- EC2 Auto Scaling
- Application Load Balancer
- Target Groups
- Launch Templates
- Amazon S3
- S3 Gateway VPC Endpoint
- AWS IAM
- Amazon CloudWatch
- Amazon SNS
- Internet Gateway
- Route Tables
- Security Groups
- GitHub Actions
- AWS STS / GitHub OIDC

## Network Design
### VPC
The VPC is deployed across two Availability Zones in the Singapore region (ap-southeast-1). EC2 application servers run only inside the private subnets. There is no direct internet route and no public IP assigned to the application servers.
<img width="1642" height="405" alt="ResourceMap" src="https://github.com/user-attachments/assets/f73f83cc-1dd5-4200-b2dc-7174107cd236" />

### Public Subnets
Public Subnet A
10.0.1.0/24
ap-southeast-1a

Public Subnet B
10.0.2.0/24
ap-southeast-1b  
The public subnets host the internet-facing Application Load Balancer.

### Private Application Subnets
Private App Subnet A
10.0.11.0/24
ap-southeast-1a

Private App Subnet B
10.0.12.0/24
ap-southeast-1b

### High Availability
The application is distributed across two Availability Zones. The Application Load Balancer distributes incoming HTTP requests between healthy EC2 targets. If one Availability Zone or EC2 instance becomes unavailable, traffic can continue through the remaining healthy instance.
<img width="1661" height="222" alt="ec2-multiAZ" src="https://github.com/user-attachments/assets/f8fea2d0-8bad-4a09-939b-d1dfc92ee028" />

### Application Load Balancer
<img width="1677" height="510" alt="alb" src="https://github.com/user-attachments/assets/1be76f20-c026-41a1-925d-2e9f56afacfe" />

### Auto Scaling
The EC2 instances are managed by an Auto Scaling Group.
Minimum capacity: 2
Desired capacity: 2
Maximum capacity: 4
<img width="1606" height="286" alt="ASG" src="https://github.com/user-attachments/assets/10f89cb6-878a-4406-8a2a-2ff6c0e161d7" />

### Self-Healing
Self-healing was tested by manually terminating one EC2 instance. The Auto Scaling Group detected that running capacity had fallen below the desired capacity and automatically launched a replacement instance. The internet-facing Application Load Balancer runs across both public subnets.

### Dynamic Auto Scaling
A Target Tracking Scaling Policy was configured using average EC2 CPU utilization. During testing, CPU load was intentionally generated against the application. The Auto Scaling Group can scale up to four instances based on workload. When utilization decreases, capacity can scale back toward the minimum of two instances.

### Monitoring
- EC2 CPUUtilization
- ALB RequestCount
- HealthyHostCount
- UnHealthyHostCount
- TargetResponseTime
<img width="1279" height="625" alt="unhealthy" src="https://github.com/user-attachments/assets/1d08079a-17ad-4dd8-9897-d0a32d26bf9d" />

### Alerting with Amazon SNS
Integrated with monitoring and Auto Scaling notifications. This provides email notifications when important infrastructure events occur.  
<img width="300" height="550" alt="WhatsApp Image 2026-09-27 at 10 50 39 PM" src="https://github.com/user-attachments/assets/7376df25-dfd7-407d-987f-bf1d6f7ed261" /> <img width="300" height="550" alt="WhatsApp Image 2026-09-27 at 10 50 40 PM" src="https://github.com/user-attachments/assets/e246a204-b9fd-43be-a8bf-8a39a90fa80b" />
### Security
The architecture separates public-facing and application resources using dedicated Security Groups.
#### 1. ALB Security Group
Allows:
HTTP :80
Source: 0.0.0.0/0

#### 2. EC2 Security Group
Alllows:
HTTP :80
Source: ALB Security Group only

### Private S3 Access
The application servers need access to Amazon S3 but are located in private subnets without a NAT Gateway.
<img width="1669" height="556" alt="endpoint" src="https://github.com/user-attachments/assets/11c4de60-4cab-412f-8038-22d6d27e4723" />

### IAM Roles and Least Privilege
EC2 instances use an IAM Instance Role instead of stored AWS credentials. The EC2 role allows the application servers to retrieve deployment files from the required S3 bucket.
<img width="1628" height="828" alt="ec2roles" src="https://github.com/user-attachments/assets/a43f1bbc-2db5-4b7d-994f-37f95c1228cf" />
### Application Deployment with S3
Application code is stored in: s3://harry-bucket-project/app/server.py  
When a new EC2 instance is launched, Launch Template User Data automatically retrieves the latest application file from S3.
### CI/CD with GitHub Actions
Automatically deploys application changes to AWS. The pipeline is triggered when files inside the "app/" directory are pushed to the main branch.
### GitHub OIDC Authentication
GitHub Actions authenticates to AWS using OpenID Connect instead of long-lived AWS access keys. This removes the need to store permanent AWS Access Key IDs and Secret Access Keys in GitHub. The IAM trust relationship is restricted to this repository and the main branch.
<img width="1609" height="812" alt="githubroles" src="https://github.com/user-attachments/assets/c21da8d7-2d5d-4691-9ba1-b2e78c7ac6e4" />
### CI Validation
Before deployment, GitHub Actions performs a Python syntax check. "python -m py_compile app/server.py"
If the Python application contains a syntax error, the deployment step does not continue.
### Rolling Deployment
After the new application is uploaded to S3, GitHub Actions starts an Auto Scaling Instance Refresh. A short instance warm-up period is configured so the application has time to start before the deployment continues.
## Project Testing
### Load Balancing Test
- Multiple requests were sent to the Application Load Balancer. Different EC2 hostnames confirmed that the ALB was distributing requests across multiple instances.
### Self-Healing Test
- One EC2 instance was manually terminated.
<img width="1586" height="324" alt="selfhealing" src="https://github.com/user-attachments/assets/03fd4045-03cc-47dd-bb48-00c197d64726" />
Result:
### Auto Scaling Group Test
- CPU workload was generated against the application.
<img width="1100" height="550" alt="cpu-utilization" src="https://github.com/user-attachments/assets/ee078697-9cc4-4b19-b4bc-de9c450d2f9f" />
<img width="1549" height="189" alt="ASG-Scaling" src="https://github.com/user-attachments/assets/0e68ec74-662c-4f83-a560-4fdc1c204eeb" />
### CI/CD Test
- The application text in "server.py" was changed and committed to the main branch.
GitHub Actions automatically:
- Validated Python
- Authenticated to AWS
- Uploaded server.py to S3
- Started an Instance Refresh
- Replaced EC2 instances
- Deployed the updated application

## More Screenshots



# What I Learned
This project provided hands-on experience with:
- Designing a highly available AWS VPC architecture
- Deploying applications across multiple Availability Zones
- Configuring Application Load Balancers and target groups
- Running EC2 servers inside private subnets
- Creating EC2 Launch Templates
- Implementing Auto Scaling and self-healing
- Testing CPU-based dynamic scaling
- Monitoring infrastructure using CloudWatch
- Configuring SNS notifications
- Applying IAM roles and least-privilege permissions
- Accessing S3 privately through a Gateway VPC Endpoint
- Deploying application artifacts through Amazon S3
- Configuring GitHub Actions
- Authenticating GitHub to AWS using OIDC
- Automating EC2 deployments through Auto Scaling Instance Refresh
- Troubleshooting AWS networking, health checks, IAM and CI/CD

## Screenshots
VPC Architecture
<img width="1601" height="386" alt="VPC Resource Map" src="https://github.com/user-attachments/assets/88ce8b5c-d3c3-4dd1-b242-92e824f74720" />

Healthy Targets
<img width="1280" height="230" alt="a99110bd-9073-472d-8c49-7a40c2bbdc07" src="https://github.com/user-attachments/assets/70ecda35-8d01-4a21-8924-cb2e99d9bf75" />

Load Balanced Application
<img width="1280" height="560" alt="WhatsApp Image 2026-08-29 at 12 00 10 AM" src="https://github.com/user-attachments/assets/1ac1cdb2-3c06-4650-aec5-0087033627de" />

Auto Scaling Recovery
<img width="1683" height="595" alt="Auto Scaling" src="https://github.com/user-attachments/assets/c7d67cdb-a1eb-4ceb-9e08-493de118da7e" />

CloudWatch Dashboard
<img width="1920" height="478" alt="cloudwatch dashboard" src="https://github.com/user-attachments/assets/d16d1a6f-20c7-4e47-abc1-bba37b6b05f3" />
