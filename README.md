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
