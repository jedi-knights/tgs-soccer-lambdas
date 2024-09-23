"""
This script is used to build the project.
It provides a set of commands to:

create a virtual environment,
install dependencies,
run linting,
run tests,
freeze dependencies,
package the project, and
clean the project directory.
"""

import os
import subprocess
import shutil

from pathlib import Path

import click

def remove_files_by_pattern(patterns: list[str]):
    """
    Remove files by pattern.

    :param patterns: A list of patterns to match.
    :return: None
    """
    for pattern in patterns:
        for path in Path(".").rglob(pattern):
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                shutil.rmtree(path)

def remove_dist_info_dirs():
    """
    Remove all directories with the .dist-info suffix.
    """
    for dist_info_dir in Path(".").rglob("*.dist-info"):
        package_dir = dist_info_dir.with_suffix("")
        shutil.rmtree(dist_info_dir)
        if package_dir.exists():
            shutil.rmtree(package_dir)

def remove_specific_dirs(dir_names: list[str]):
    """
    Remove specific directories from the project directory.

    :param dir_names: A list of directory names to remove.
    :return: None
    """
    for dir_name in dir_names:
        for path in Path(".").rglob(dir_name):
            if path.is_dir() and ".venv" not in path.parts:
                shutil.rmtree(path)

def remove_specific_files(file_names: list[str]):
    """
    Remove specific files from the project directory.

    :param file_names: A list of file names to remove.
    :return: None
    """
    for file_name in file_names:
        for path in Path(".").rglob(file_name):
            if path.is_file() and ".venv" not in path.parts:
                path.unlink()

@click.group()
def cli():
    """
    A python CLI tool to build the project.
    """


def package_lambda(lambda_dir: str,
                   staging_dir: str = 'staging',
                   dependencies_dir: str = 'dependencies',
                   delete_staging_after: bool = False) -> str:
    """
    This function packages a specified lambda directory into an archive.

    :lamba_dir: str
    :staging_dir: str
    :dependencies_dir: str
    :delete_staging_after: bool
    :returns str archive name
    """
    if lambda_dir is None:
        raise ValueError('The lambda directory is required.')

    if not os.path.isdir(lambda_dir):
        raise ValueError(f'The lambda directory "{lambda_dir}" does not exist.')

    if not os.path.isdir(dependencies_dir):
        raise ValueError(f'The dependencies directory "{dependencies_dir}" does not exist.')

    # Delete the staging directory if it already exists.
    if os.path.isdir(staging_dir):
        shutil.rmtree(staging_dir)

    # Create an empty staging directory
    os.mkdir(staging_dir)

    # If the dependencies directory exists then copy it into the staging directory
    if os.path.isdir(dependencies_dir):
        shutil.copytree(src=dependencies_dir, dst=staging_dir, dirs_exist_ok=True)

    # Copy lambda directory into the staging directory.
    shutil.copytree(src=lambda_dir, dst=staging_dir, dirs_exist_ok=True)

    # Create the archive file from the staging directory.
    archive_name = shutil.make_archive(base_name=lambda_dir, format='zip', root_dir=staging_dir)

    # Problem: This is not creating the archive at the root of the project.
    #          The archive is appearing in the 'lambda_functions' directory.
    # I may need to move each archive after it's created unless there's a way to instruct the
    # make_archive function to put it at the root.

    if delete_staging_after:
        # Delete the staging directory.
        shutil.rmtree(staging_dir)

    return archive_name


@cli.command()
def package_project():
    """Package the project."""
    try:
        if not os.path.exists("dependencies"):
            args = [
                "pip3",
                "install",
                "-r",
                "requirements.txt",
                "-t",
                "dependencies/"
            ]
            subprocess.run(args, check=True)

        shutil.copytree("dependencies", "layer/python/common", dirs_exist_ok=True)
        shutil.make_archive("common_layer", "zip", "layer/python/common")

        lambda_dirs = []
        for item in os.listdir("lambda_functions"):
            if os.path.isdir(os.path.join("lambda_functions", item)):
                lambda_dirs.append(item)

        for lambda_dir in lambda_dirs:
            src = "dependencies"
            dst = os.path.join("lambda_functions", lambda_dir)
            shutil.copytree(src, dst, dirs_exist_ok=True)
            shutil.make_archive(lambda_dir, "zip", os.path.join("lambda_functions", lambda_dir))
    except (subprocess.CalledProcessError, shutil.Error) as err:
        click.echo(f"Failed to package the project: {err}")

@cli.command()
def build_project():
    """Build the project."""
    clean_project()
    package_project()

@cli.command()
def clean_project():
    """Clean the project directory."""
    specific_dirs = [
        "_pytest",
        "bin",
        "boto3",
        "botocore",
        "bs4",
        "certifi",
        "charset_normalizer",
        "dateutil",
        "idna",
        "iniconfig",
        "jmespath",
        "pluggy",
        "pytest",
        "requests",
        "s3transfer",
        "soupsieve",
        "urllib3"
    ]

    specific_files = [
        "pipe.py",
        "py.py",
        "README.rst",
        "six.py"
    ]

    try:
        remove_dist_info_dirs()
        remove_specific_dirs(specific_dirs)
        remove_specific_files(specific_files)
    except (shutil.Error, OSError) as err:
        click.echo(f"Failed to clean the project directory: {err}")

if __name__ == "__main__":
    cli()
