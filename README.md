# tgs-soccer-lambdas

## Conventional Commits Cheat Sheet

```plaintext
<type>[optional scope]: <description>

[optional body]

[optional footer]
```

# Quick examples
* `feat: new feature`
* `fix(scope): bug in scope`
* `feat!: breaking change` / `feat(scope)!: rework API`
* `chore(deps): update dependencies`

# Commit types
* `build`: Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)
* `ci`: Changes to CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs)
* **`chore`: Changes which doesn't change source code or tests e.g. changes to the build process, auxiliary tools, libraries**
* `docs`: Documentation only changes
* **`feat`: A new feature**
* **`fix`: A bug fix**
* `perf`: A code change that improves performance
* `refactor`:  A code change that neither fixes a bug nor adds a feature
* `revert`: Revert something
* `style`: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
* `test`: Adding missing tests or correcting existing tests

# Reminders
* Put newline before extended commit body
* More details at **[conventionalcommits.org](https://www.conventionalcommits.org/)**

## Directory Structure

```plaintext
lambda-cloudformation-deployment/
├── common/
│   ├── __init__.py            # Common code for all Lambdas
│   └── utils.py               # Utility functions shared across Lambdas
├── lambda_functions/
│   ├── tgs_get_clubs_by_organization/
│   │   └── app.py             # Code for tgs_get_clubs_by_organization Lambda
│   ├── tgs_get_countries/
│   │   └── app.py             # Code for tgs_get_countries Lambda
│   ├── tgs_get_match_records/
│   │   └── app.py             # Code for tgs_get_match_records Lambda
│   ├── tgs_get_organizations/
│   │   └── app.py             # Code for tgs_get_organizations Lambda
│   └── tgs_get_states/
│       └── app.py             # Code for tgs_get_states Lambda
├── cloudformation_templates/
│   ├── lambda_template.yaml   # CloudFormation template for Lambda functions
│   └── layer_template.yaml    # CloudFormation template for the common layer (if using layers)
├── .github/
│   └── workflows/
│       └── deploy-lambda.yml  # GitHub Actions workflow for Lambda deployment
├── README.md                  # Documentation
├── requirements.txt           # Python dependencies (optional)
└── setup.py                   # Package setup (if needed)
```


I am opting to share dependencies across all my lambda functions so I will have a single requirements.txt file at the 
root of my repository.

When deploying, I will install the dependencies and package them with each Lambda function:

```shell
pip install -r requirements.txt -t lambda_functions/get_clubs_by_organization/
cd lambda_functions/get_clubs_by_organization/
zip -r my_function.zip .
```

When you zip your Lambda function, include the common directory:

```shell
zip -r my_function.zip lambda_functions/my_function/ common/
```

This project contains source code and supporting files for a serverless application that you can deploy with the SAM CLI. It includes the following files and folders.

- hello_world - Code for the application's Lambda function.
- events - Invocation events that you can use to invoke the function.
- tests - Unit tests for the application code. 
- template.yaml - A template that defines the application's AWS resources.

The application uses several AWS resources, including Lambda functions and an API Gateway API. These resources are defined in the `template.yaml` file in this project. You can update the template to add AWS resources through the same deployment process that updates your application code.

If you prefer to use an integrated development environment (IDE) to build and test your application, you can use the AWS Toolkit.  
The AWS Toolkit is an open source plug-in for popular IDEs that uses the SAM CLI to build and deploy serverless applications on AWS. The AWS Toolkit also adds a simplified step-through debugging experience for Lambda function code. See the following links to get started.

* [CLion](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [GoLand](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [IntelliJ](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [WebStorm](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [Rider](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [PhpStorm](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [PyCharm](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [RubyMine](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [DataGrip](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [VS Code](https://docs.aws.amazon.com/toolkit-for-vscode/latest/userguide/welcome.html)
* [Visual Studio](https://docs.aws.amazon.com/toolkit-for-visual-studio/latest/user-guide/welcome.html)

## Deploy the sample application

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda. It can also emulate your application's build environment and API.

To use the SAM CLI, you need the following tools.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

To build and deploy your application for the first time, run the following in your shell:

```bash
sam build --use-container
sam cloudformation_templates --guided
```

The first command will build the source of your application. The second command will package and deploy your application to AWS, with a series of prompts:

* **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region, and a good starting point would be something matching your project name.
* **AWS Region**: The AWS region you want to deploy your app to.
* **Confirm changes before deploy**: If set to yes, any change sets will be shown to you before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes.
* **Allow SAM CLI IAM role creation**: Many AWS SAM templates, including this example, create AWS IAM roles required for the AWS Lambda function(s) included to access AWS services. By default, these are scoped down to minimum required permissions. To deploy an AWS CloudFormation stack which creates or modifies IAM roles, the `CAPABILITY_IAM` value for `capabilities` must be provided. If permission isn't provided through this prompt, to deploy this example you must explicitly pass `--capabilities CAPABILITY_IAM` to the `sam deploy` command.
* **Save arguments to samconfig.toml**: If set to yes, your choices will be saved to a configuration file inside the project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your application.

You can find your API Gateway Endpoint URL in the output values displayed after deployment.

## Use the SAM CLI to build and test locally

Build your application with the `sam build --use-container` command.

```bash
tgs-soccer-lambdas$ sam build --use-container
```

The SAM CLI installs dependencies defined in `hello_world/requirements.txt`, creates a deployment package, and saves it in the `.aws-sam/build` folder.

Test a single function by invoking it directly with a test event. An event is a JSON document that represents the input that the function receives from the event source. Test events are included in the `events` folder in this project.

Run functions locally and invoke them with the `sam local invoke` command.

```bash
tgs-soccer-lambdas$ sam local invoke HelloWorldFunction --event events/empty.json
```

The SAM CLI can also emulate your application's API. Use the `sam local start-api` to run the API locally on port 3000.

```bash
tgs-soccer-lambdas$ sam local start-api
tgs-soccer-lambdas$ curl http://localhost:3000/
```

The SAM CLI reads the application template to determine the API's routes and the functions that they invoke. The `Events` property on each function's definition includes the route and method for each path.

```yaml
      Events:
        HelloWorld:
          Type: Api
          Properties:
            Path: /hello
            Method: get
```

## Add a resource to your application
The application template uses AWS Serverless Application Model (AWS SAM) to define application resources. AWS SAM is an extension of AWS CloudFormation with a simpler syntax for configuring common serverless application resources such as functions, triggers, and APIs. For resources not included in [the SAM specification](https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md), you can use standard [AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html) resource types.

## Fetch, tail, and filter Lambda function logs

To simplify troubleshooting, SAM CLI has a command called `sam logs`. `sam logs` lets you fetch logs generated by your deployed Lambda function from the command line. In addition to printing the logs on the terminal, this command has several nifty features to help you quickly find the bug.

`NOTE`: This command works for all AWS Lambda functions; not just the ones you deploy using SAM.

```bash
tgs-soccer-lambdas$ sam logs -n HelloWorldFunction --stack-name "tgs-soccer-lambdas" --tail
```

You can find more information and examples about filtering Lambda function logs in the [SAM CLI Documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-logging.html).

## Tests

Tests are defined in the `tests` folder in this project. Use PIP to install the test dependencies and run tests.

```bash
tgs-soccer-lambdas$ pip install -r events/requirements.txt --user
# unit test
tgs-soccer-lambdas$ python -m pytest events/unit -v
# integration test, requiring deploying the stack first.
# Create the env variable AWS_SAM_STACK_NAME with the name of the stack we are testing
tgs-soccer-lambdas$ AWS_SAM_STACK_NAME="tgs-soccer-lambdas" python -m pytest events/integration -v
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
sam delete --stack-name "tgs-soccer-lambdas"
```

Commands you can use next
=========================
[*] Create pipeline: cd tgs-soccer-lambdas && sam pipeline init --bootstrap
[*] Validate SAM template: cd tgs-soccer-lambdas && sam validate
[*] Test Function in the Cloud: cd tgs-soccer-lambdas && sam sync --stack-name {stack-name} --watch

```text
aws-lambda-soccer/
│
├── functions/
│   ├── get_states/
│   │   ├── app.py              # Lambda function to fetch states data
│   │   ├── requirements.txt    # Dependencies for the get_states function
│   │   └── .env                # Environment variables (e.g., API keys)
│   ├── get_countries/
│   │   ├── app.py              # Lambda function to fetch countries data
│   │   ├── requirements.txt    # Dependencies for the get_countries function
│   ├── get_organizations/
│   │   ├── app.py              # Lambda function to fetch organizations
│   │   ├── requirements.txt    # Dependencies for the get_organizations function
│   ├── get_clubs_in_organization/
│   │   ├── app.py              # Lambda function to fetch clubs within an organization
│   │   ├── requirements.txt    # Dependencies for the get_clubs_in_organization function
│   ├── get_match_records/
│   │   ├── app.py              # Lambda function to fetch match records between two dates
│   │   ├── requirements.txt    # Dependencies for the get_match_records function
│   └── ...
│
├── common/
│   ├── total_global_sports_api.py  # Code to handle the API interaction with Total Global Sports
│   ├── config.py                  # Configuration shared across multiple functions
│   └── utils.py                   # Utility functions (e.g., date formatting, validation)
│
├── deploy/
│   ├── sam-template.yaml           # AWS SAM template for deploying the Lambda functions
│   └── serverless.yml              # Optional: if using the Serverless Framework
│
├── .gitignore                      # Ignore unnecessary files (e.g., .env, __pycache__)
├── README.md                       # Description of the repository and usage
└── requirements.txt                # Optional: top-level dependencies for all Lambda functions
```

## Packaging

Your AWS Lambda function’s code comprises a .py file containing your function’s handler code, together with any 
additional packages and modules your code depends on. To deploy this function code to Lambda, you use a deployment 
package. This package may either be a .zip file archive or a container image. 

To create your deployment package as .zip file archive, you can use your command-line tool’s built-in .zip file 
archive utility, or any other .zip file utility such as 7zip.

Note that Lambda uses POSIX file permissions, so you may need to set permissions for the deployment package folder 
before you create the .zip file archive.

## Resources

- [Working with layers for Python Lambda functions](https://docs.aws.amazon.com/lambda/latest/dg/python-layers.html)
- [Packaging your layer content](https://docs.aws.amazon.com/lambda/latest/dg/packaging-layers.html)
- [Creating and updating Python Lambda functions using .zip files](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html#python-package-create-update)
- [Working with .zip file archives for Python Lambda functions](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html)
- [Packaging your layer content](https://docs.aws.amazon.com/lambda/latest/dg/packaging-layers.html)
- [Working with layers for Python Lambda functions](https://docs.aws.amazon.com/lambda/latest/dg/python-layers.html)
- [Define Lambda function handler in Python](https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html)
- [AWS Lambda Function](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html)
- [AWS Lambda API Reference](https://docs.aws.amazon.com/lambda/latest/api/welcome.html)
- [Lambda Runtimes](https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html)
