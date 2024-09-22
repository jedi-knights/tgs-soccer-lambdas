#!/bin/bash

# Variables
STACK_NAME="LambdaExecutionRoleStack"
SCRIPT_DIR=$(dirname "$0")
TEMPLATE_FILE="$SCRIPT_DIR/../cloudformation_templates/lambda_execution_role.yaml"
REGION="us-east-1"

# Create the stack
aws cloudformation create-stack \
  --stack-name $STACK_NAME \
  --template-body file://$TEMPLATE_FILE \
  --region $REGION \
  --capabilities CAPABILITY_NAMED_IAM

# Wait for the stack to be created
aws cloudformation wait stack-create-complete \
  --stack-name $STACK_NAME \
  --region $REGION

echo "Stack $STACK_NAME created successfully."