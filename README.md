# Highly Available Web Application on AWS

A hands-on AWS cloud project designed to demonstrate high availability,
load balancing, fault tolerance, Auto Scaling and infrastructure monitoring.

## Architecture

The application is deployed across two Availability Zones using an
Application Load Balancer and EC2 instances managed by an Auto Scaling Group.

```mermaid
flowchart TD

    User[Internet User] --> ALB[Application Load Balancer]

    subgraph VPC[AWS VPC]

        subgraph AZ1[Availability Zone A]
            PublicA[Public Subnet A]
            PrivateA[Private App Subnet A]
            EC2A[EC2 Instance]
        end

        subgraph AZ2[Availability Zone B]
            PublicB[Public Subnet B]
            PrivateB[Private App Subnet B]
            EC2B[EC2 Instance]
        end

        ALB --> PublicA
        ALB --> PublicB

        ALB --> EC2A
        ALB --> EC2B

        EC2A --> PrivateA
        EC2B --> PrivateB

    end

    ASG[Auto Scaling Group] --> EC2A
    ASG --> EC2B

    EC2A --> CW[Amazon CloudWatch]
    EC2B --> CW
    ALB --> CW

AWS Services Used
Amazon VPC
EC2
Application Load Balancer
Auto Scaling Group
Launch Templates
Security Groups
Internet Gateway
Route Tables
CloudWatch
Network Design

The architecture uses two Availability Zones for high availability.

Public subnets host the internet-facing Application Load Balancer.
EC2 application servers are deployed in private subnets.
EC2 instances accept HTTP traffic only from the ALB security group.
No direct public access is provided to the EC2 instances.
No NAT Gateway was required for this project.
High Availability

Two EC2 instances are distributed across separate Availability Zones.

The Application Load Balancer distributes incoming HTTP requests across
healthy targets in both Availability Zones.

Auto Scaling and Self-Healing

The EC2 instances are managed by an Auto Scaling Group with a desired
capacity of two instances.

During testing, an EC2 instance was intentionally terminated.

The Auto Scaling Group detected the loss of capacity and automatically
launched a replacement instance while the remaining healthy instance
continued serving traffic.

Monitoring

Amazon CloudWatch was configured to monitor:

RequestCount
HealthyHostCount
UnHealthyHostCount
TargetResponseTime
EC2 CPUUtilization

CloudWatch alarms were also configured for unhealthy targets and high
CPU utilization.

Security

Separate security groups were configured for the load balancer and EC2
application servers.

Internet traffic:

Internet → ALB → EC2

The EC2 security group accepts HTTP traffic only from the Application
Load Balancer security group.

What I Learned

This project helped me gain hands-on experience with:

VPC and subnet design
Multi-AZ cloud architecture
Application Load Balancing
EC2 Launch Templates
Auto Scaling
Health checks and automatic instance replacement
Security Group configuration
CloudWatch monitoring
Troubleshooting AWS infrastructure
Screenshots
VPC Architecture

Healthy Targets

Load Balanced Application

Auto Scaling Recovery

CloudWatch Dashboard
