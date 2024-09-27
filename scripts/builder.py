"""
This script is used to build the project.
It provides a set of commands to:

create a virtual environment,
install dependencies,
run linting,
run events,
freeze dependencies,
package the project, and
clean the project directory.
"""

import os
import stat
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

def find_root_dir() -> str:
    """
    Find the root directory of the project.

    :return: str
    """
    current_dir = os.getcwd()
    while not os.path.exists(os.path.join(current_dir, ".git")):
        parent_dir = os.path.dirname(current_dir)
        if current_dir == parent_dir:
            raise FileNotFoundError("The root directory could not be found.")

        current_dir = parent_dir

    return current_dir

def validate_directories(lambda_dir: str, dependencies_dir: str):
    """
    Validate the lambda and dependencies directories.

    :param lambda_dir:
    :param dependencies_dir:
    :return:
    """
    if lambda_dir is None:
        raise ValueError('The lambda directory is required.')

    if not os.path.isdir(lambda_dir):
        raise ValueError(f'The lambda directory "{lambda_dir}" does not exist.')

    if not os.path.isdir(dependencies_dir):
        raise ValueError(f'The dependencies directory "{dependencies_dir}" does not exist.')


def set_permissions(path: str):
    """
    Set POSIX file permissions for the given path.

    :param path: The path to set permissions for.
    """
    for root, dirs, files in os.walk(path):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            os.chmod(dir_path,
                     stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)

        for file_name in files:
            file_path = os.path.join(root, file_name)
            os.chmod(file_path,
                     stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)


def prepare_staging_directory(staging_dir: str):
    """
    Prepare the staging directory.

    :param staging_dir:
    :return:
    """
    if os.path.isdir(staging_dir):
        shutil.rmtree(staging_dir)

    os.mkdir(staging_dir)
    set_permissions(staging_dir)

def copy_directory(src: str, dst: str):
    """
    Copy the source directory to the destination directory.

    :param src:
    :param dst:
    :return:
    """
    shutil.copytree(src=src, dst=dst, dirs_exist_ok=True)
    set_permissions(dst)


def copy_directories(lambda_dir: str, dependencies_dir: str, staging_dir: str):
    """
    Copy the lambda and dependencies directories into the staging directory.

    :param lambda_dir:
    :param dependencies_dir:
    :param staging_dir:
    :return:
    """
    if os.path.isdir(dependencies_dir):
        copy_directory(src=dependencies_dir, dst=staging_dir)

    copy_directory(src=lambda_dir, dst=staging_dir)


def create_archive(lambda_dir: str, staging_dir: str, root_dir: str) -> str:
    """
    Create an archive from the lambda directory.

    :param lambda_dir:
    :param staging_dir:
    :param root_dir:
    :return:
    """
    base_name = os.path.join(root_dir, os.path.basename(lambda_dir))
    archive_name = shutil.make_archive(base_name=base_name, format='zip', root_dir=staging_dir)
    return archive_name

def _install_dependencies(dependencies_dir: str = 'dependencies'):
    """Install dependencies from requirements.txt to the dependencies/ directory."""
    if os.path.exists(dependencies_dir):
        click.echo("Dependencies directory already exists. No action taken.")
        return

    try:
        os.makedirs(dependencies_dir)
        args = [
            "pip3",
            "install",
            "-r",
            "requirements.txt",
            "-t",
            "dependencies/"
        ]
        subprocess.run(args, check=True)
        click.echo("Dependencies installed successfully.")
    except subprocess.CalledProcessError as err:
        click.echo(f"Failed to install dependencies: {err}")


@cli.command(name='deps')
@click.option('--dependencies-dir', default='dependencies', help='The dependencies directory.')
def install_dependencies(dependencies_dir: str = 'dependencies'):
    """Install dependencies from requirements.txt to the dependencies/ directory."""
    _install_dependencies(dependencies_dir)
    click.echo(f"Dependencies installed successfully to '{dependencies_dir}'.")


def _pack(lambda_dir: str,
         staging_dir: str = 'staging',
         python_version: str = 'python3.12',
         dependencies_dir: str = 'dependencies',
         delete_staging_after: bool = False) -> str:
    """
    This function packages a specified lambda directory into an archive.

    :param lambda_dir:
    :param staging_dir:
    :param dependencies_dir:
    :param delete_staging_after:
    :param is_layer:
    :return:
    """
    is_layer = 'layers' in lambda_dir

    if not os.path.exists(dependencies_dir):
        _install_dependencies(dependencies_dir)

    validate_directories(lambda_dir, dependencies_dir)
    prepare_staging_directory(staging_dir)

    root_dir = find_root_dir()

    python_dir = os.path.join(staging_dir, 'python')
    copy_directory(lambda_dir, python_dir)

    if is_layer:
        # handle the layers case
        site_packages = os.path.join(python_dir, 'lib', python_version, 'site-packages')
        os.makedirs(site_packages)
        copy_directory(dependencies_dir, site_packages)

    archive_name = create_archive(lambda_dir, staging_dir, root_dir)

    if delete_staging_after:
        shutil.rmtree(staging_dir)

    return archive_name

@cli.command()
@click.argument('lambda_dir')
@click.option('--staging-dir', default='staging', help='The staging directory.')
@click.option('--dependencies-dir', default='dependencies', help='The dependencies directory.')
@click.option('--python-version', default='python3.12', help='The Python version.')
@click.option('--delete-staging-after', is_flag=True, help='Delete staging directory after.')
def pack(lambda_dir: str,
         staging_dir: str = 'staging',
         dependencies_dir: str = 'dependencies',
         python_version: str = 'python3.12',
         delete_staging_after: bool = False):
    """
    This function packages a specified lambda directory into an archive.

    :param lambda_dir:
    :param staging_dir:
    :param dependencies_dir:
    :param delete_staging_after:
    :return:
    """
    archive_name = _pack(lambda_dir,
                         staging_dir,
                         python_version,
                         dependencies_dir,
                         delete_staging_after)
    click.echo(f"Lambda packaged successfully: {archive_name}")


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

        shutil.copytree("dependencies", "layers/python/common", dirs_exist_ok=True)
        shutil.make_archive("common_layer", "zip", "layers/python/common")

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
