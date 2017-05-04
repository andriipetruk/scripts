#!/bin/bash

# get region
REGION=$(curl -s http://169.254.169.254/latest/dynamic/instance-identity/document|grep region|awk -F\" '{print $4}')

# get instance-id from meta-data, if you like:
INSTANCE_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)

# get stack name
aws ec2 describe-instances \
  --region $REGION   \
  --instance-id $INSTANCE_ID \
  --query 'Reservations[*].Instances[*].Tags[?Key==`aws:cloudformation:stack-name`].Value' \
  --output text
