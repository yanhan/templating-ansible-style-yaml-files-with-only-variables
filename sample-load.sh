#!/bin/bash

set -euo pipefail
IFS=$'\n\t'

main() {
  set +u
  . venv/bin/activate
  set -u

  python load.py

  set +u
  deactivate
  set -u
}

main "$@"
