# About

Illustrates how to template Ansible-style YAML files that only contain variables, using Ansible's codebase.

Accompanying blog post: http://blog.pangyanhan.com/posts/2015-12-12-how-to-template-ansible-style-yaml-files-that-only-contain-variables.html

## Setup

    ./setup.sh

## Sample Run

    ./sample-run.sh

## How to run this in general

To dump the output as JSON (recommended):

    . venv/bin/activate
    python main.py folder_with_yaml_files
    deactivate

To dump the output as YAML:

    . venv/bin/activate
    python main.py folder_with_yaml_files --output-as-yaml
    deactivate

## Purpose of the `load.py` file

The `load.py` file shows how to load a YAML file output by the `main.py` file.

Usage:

    . venv/bin/acitvate
    python load.py input_yaml_file
    deactivate
