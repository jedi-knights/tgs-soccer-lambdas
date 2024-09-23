from scripts.builder import package_lambda

if __name__ == "__main__":
    archive_name = package_lambda('lambda_functions/get_states',
                                  'staging',
                                  'dependencies',
                                  False)

    print(f'Created the archive "{archive_name}"')


