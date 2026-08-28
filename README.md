# Highly Available Web Application on AWS

A hands-on AWS cloud project designed to demonstrate high availability,
load balancing, fault tolerance, Auto Scaling and infrastructure monitoring.

## Architecture

The application is deployed across two Availability Zones using an
Application Load Balancer and EC2 instances managed by an Auto Scaling Group.

**AWS Services Used**
- Amazon VPC
- EC2
- Application Load Balancer
- Auto Scaling Group
- Launch Templates
- Security Groups
- Internet Gateway
- Route Tables
- CloudWatch

**Network Design**
The architecture uses two Availability Zones for high availability.
- Public subnets host the internet-facing Application Load Balancer.
- EC2 application servers are deployed in private subnets.
- EC2 instances accept HTTP traffic only from the ALB security group.
- No direct public access is provided to the EC2 instances.
- No NAT Gateway was required for this project.

**High Availability**
Two EC2 instances are distributed across separate Availability Zones. The Application Load Balancer distributes incoming HTTP requests across healthy targets in both Availability Zones.

**Auto Scaling and Self-Healing**
The EC2 instances are managed by an Auto Scaling Group with a desired capacity of two instances.

During testing, an EC2 instance was intentionally terminated. The Auto Scaling Group detected the loss of capacity and automatically launched a replacement instance while the remaining healthy instance continued serving traffic.

**Monitoring**
Amazon CloudWatch was configured to monitor:
- RequestCount
- HealthyHostCount
- UnHealthyHostCount
- TargetResponseTime
- EC2 CPUUtilization
CloudWatch alarms were also configured for unhealthy targets and high CPU utilization.

**Security**
Separate security groups were configured for the load balancer and EC2 application servers.

Internet traffic:
Internet → ALB → EC2

The EC2 security group accepts HTTP traffic only from the Application Load Balancer security group.

What I Learned

This project helped me gain hands-on experience with:
- VPC and subnet design
- Multi-AZ cloud architecture
- Application Load Balancing
- EC2 Launch Templates
- Auto Scaling
- Health checks and automatic instance replacement
- Security Group configuration
- CloudWatch monitoring
- Troubleshooting AWS infrastructure

**Screenshots**
VPC Architecture
<img width="1280" height="560" alt="image" src="https://github.com/user-attachments/assets/3cb2e3d6-f381-4716-ac4b-e6853052608a" />

Healthy Targets
<img width="1280" height="230" alt="a99110bd-9073-472d-8c49-7a40c2bbdc07" src="https://github.com/user-attachments/assets/70ecda35-8d01-4a21-8924-cb2e99d9bf75" />

Load Balanced Application
![Uploading image.png…]()

Auto Scaling Recovery

CloudWatch Dashboard
