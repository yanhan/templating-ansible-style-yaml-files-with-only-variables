import argparse
import os.path
import sys
# The following line allows us to use the `ansible` codebase.
# This is required because Ansible data structures are dumped into the output
# file by `main.py` (instead of "plain" YAML data structures which can be
# represented by native Python data structures).
sys.path.append(os.path.join(os.getcwd(), "ansible", "lib"))

import ansible
import yaml

def _main():
  parser = argparse.ArgumentParser(
    description="Loads a YAML file with Ansible data structures and prints them to standard output",
  )
  parser.add_argument(
    "--input-file",
    dest="input_file",
    default="sample_output.yml",
    help="The input YAML file to read from",
  )
  args = parser.parse_args()
  with open(args.input_file, "r") as f:
    print yaml.load(f.read())

if __name__ == "__main__":
  _main()
