#!/bin/bash

# Check if stack_name argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <stack_name>"
  exit 1
fi

# Assign the first argument to stack_name
stack_name=$1

# Display the stack events
aws cloudformation describe-stack-events --stack-name "$stack_name"
