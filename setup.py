from setuptools import setup, find_packages

# Read the README file for long description (optional)
with open("README.md", "r") as fh:
    long_description = fh.read()

# Read the requirements.txt file
with open("requirements.txt", "r") as fh:
    requirements = fh.readlines()

# Filter non-development dependencies
non_dev_requirements = [
    req.strip() for req in requirements if req.strip() and not req.startswith((
        "pytest", "pylint", "flake8", "black", "mypy"
    ))
]

setup(
    name="tgs_soccer_lambdas",  # Package name
    version="0.1.0",  # Initial version
    author="Omar Crosby",
    author_email="omar.crosby@gmail.com",
    description="AWS Lambda functions to retrieve Soccer data",  # Brief description
    long_description=long_description,  # From README.md
    long_description_content_type="text/markdown",  # If you're using Markdown for README
    url="https://github.com/jedi-knights/tgs-soccer-lambdas",  # GitHub URL
    packages=find_packages(),  # Automatically find packages in this directory
    install_requires=non_dev_requirements,
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
