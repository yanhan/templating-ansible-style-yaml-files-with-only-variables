import argparse
import os
import os.path
import sys
# The following line allows us to use the `ansible` codebase.
sys.path.append(os.path.join(os.getcwd(), "ansible", "lib"))

from ansible.errors import AnsibleUndefinedVariable
from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar

def _main():
  parser = argparse.ArgumentParser(
    description="template Ansible style YAML files that only contain variables, using Ansible's codebase",
  )
  parser.add_argument(
    "yaml_files_dir",
    help="folder where the YAML files to template are stored",
  )
  parser.add_argument(
    "--output-as-yaml",
    dest="output_as_yaml",
    action="store_true",
    help="Output resulting variables as YAML instead of JSON",
  )
  args = parser.parse_args()

  # Load variables from the YAML files
  yaml_files_dir = os.path.join(args.yaml_files_dir)
  var_files = [
    os.path.join(yaml_files_dir, file_name)
      for file_name in os.listdir(yaml_files_dir)
  ]
  dl = DataLoader()
  vars_to_template = dict()
  for var_file in var_files:
    vars_to_template.update(dl.load_from_file(var_file))

  templar = Templar(loader=dl)
  result_vars = dict()
  # because some variables depend on the value of other variables and we don't
  # want to spend the effort to do a topological sort on them, we adopt the
  # following strategy:
  #
  # 1. maintain a dict of all successfully templated variables in `result_vars`
  # 2. until the `vars_to_template` dict is empty, do the following:
  #
  #    Try templating each variable using `ansible.template.Templar.template`.
  #
  #    If we get a `AnsibleUndefinedVariable` error, this means that the current
  #    variable depends on another variable. We ignore the error and keep the
  #    variable around for a future round of templating.
  #
  #    Otherwise, we have successfully templated the variable and add it to the
  #    `result_vars` variable. We also add the variable name to the
  #    `successfully_templated_vars` list.
  #
  #    At the end of each templating round, remove all variables in
  #    `successfully_templated_vars` from `vars_to_template`.
  #
  #
  # Note that the above algorithm will only work if all variables required for
  # interpolation are present. Otherwise, it will be stuck in an infinite loop.
  while vars_to_template:
    successfully_templated_vars = []
    for var_name, value in vars_to_template.items():
      try:
        templated_value = templar.template(value)
        result_vars[var_name] = templated_value
        successfully_templated_vars.append(var_name)
        templar.set_available_variables(result_vars.copy())
      except AnsibleUndefinedVariable:
        pass
    for var_name in successfully_templated_vars:
      del vars_to_template[var_name]

  if args.output_as_yaml:
    # NOTE: While it seems from printing `result_vars` that the most fundamental
    #       values are strings, they are in fact
    #       `ansible.parsing.yaml.objects.AnsibleUnicode` objects. Hence when
    #       we use `yaml.dump` to serialize `result_vars`, we get some rather
    #       intimidating-looking stuff that may make it seem like we've gotten
    #       an error when in fact we haven't. So do not be too alarmed by the
    #       voluminous output.
    import yaml
    print yaml.dump(result_vars)
  else:
    import json
    print json.dumps(result_vars)

if __name__ == "__main__":
  _main()
