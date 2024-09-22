#!/bin/bash

# Variables
STACK_NAME="LambdaExecutionRoleStack"
REGION="us-east-1"

# Delete the stack
aws cloudformation delete-stack \
  --stack-name $STACK_NAME \
  --region $REGION

# Wait for the stack to be deleted
aws cloudformation wait stack-delete-complete \
  --stack-name $STACK_NAME \
  --region $REGION

echo "Stack $STACK_NAME deleted successfully."
