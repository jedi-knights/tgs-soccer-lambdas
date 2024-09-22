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
