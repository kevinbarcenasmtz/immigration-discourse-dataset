#!/bin/bash
# Temporary AWS credentials (session only)
# Source this file: source setup_aws.sh

echo "Enter AWS Access Key ID:"
read AWS_ACCESS_KEY_ID
echo "Enter AWS Secret Access Key:"
read -s AWS_SECRET_ACCESS_KEY  # -s hides typing

export AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY
export AWS_DEFAULT_REGION=us-east-1

echo "AWS credentials set for this session"
echo "They will be cleared when you close this terminal"