#!/bin/bash

set -euo pipefail
IFS=$'\n\t'

main() {
  set +u
  . venv/bin/activate
  set -u

  python main.py yaml_files

  set +u
  deactivate
  set -u
}

main "$@"
