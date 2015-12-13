#!/bin/bash

set -euo pipefail
IFS=$'\n\t'

main() {
  if [ ! -d venv ]
  then
    virtualenv venv
  fi

  set +u
  . venv/bin/activate
  pip install -r requirements.txt
  deactivate
  set -u

  git submodule init
  git submodule update
}

main "$@"
