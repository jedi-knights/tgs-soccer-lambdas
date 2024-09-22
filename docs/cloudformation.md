# Cloud Formation

## Notes

Display the events of a stack:

"""shell
aws cloudformation describe-stack-events --stack-name <stack-name>
"""

Note: The `--stack-name` parameter is optional. If not provided, all stacks will be displayed.

Note: This is a paginated command. Use the `--max-items` parameter to control the number of items displayed.

Note: This is useful to see the progress of a stack creation or update.


