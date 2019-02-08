#!/usr/bin/env python

import pprint
import os

import ruamel.yaml

yaml = ruamel.yaml.YAML()


from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-f", "--file",
                    dest="filename",
                    required=True,
                    help="Source file for the THT config being converted")
parser.add_argument("-r", "--role-name",
                    dest="role_name",
                    required=True,
                    help="The name of the THT role to be converted")
parser.add_argument("-t", "--task-name",
                    dest="task_name",
                    required=True,
                    help="The task to extract from the THT role file and "
                         "write out as an Ansible role")
parser.add_argument("-o", "--overwrite",
                    dest="overwrite", action='store_true',
                    default=False,
                    help="If this option is provided, and the destination "
                         "directory exists, overwrite the contents")

args = parser.parse_args()

pp = pprint.PrettyPrinter(width=76)


def yaml_load(filepath):
    """ Loads YAML from a file """
    with open(filepath, "r") as file_descriptor:
        data = yaml.load(file_descriptor)
    return data


def yaml_dump(filepath, data):
    """ Dumps YAML to a file """
    with open(filepath, "w") as file_descriptor:
        yaml.dump(data, file_descriptor)


def write_role_data(role_dir, task_name, task_data):
    """ Write data extract to new role """
    try:
        output_dir = role_dir+'/tasks/'
        output_file = output_dir+task_name+'.yml'
        if os.path.exists(role_dir) and overwrite:
            print("Override set, writing to existing dir.")
            yaml_dump(output_file, task_data)
        elif os.path.exists(role_dir):
            print("{} already exists, skipping. Set the overwrite flag (-o) "
                  "to ignore this error.".format(role_dir))
        else:
            # if the dir doesnt exist, make it and write yaml in it
            os.makedirs(output_dir)
            yaml_dump(output_file, task_data)
    except os.error as e:
        print("I can't write here, because {}".format(e))

    # Ansible requires at least an empty main.yaml in the task dir
    if not os.path.isfile(output_dir + '/main.yml'):
        os.mknod(output_dir+'/main.yml')

## TODO: Add function to copy source file to new yaml with extract removed
##       and import in its place
## watch for: formatting retention in nested flow sections, unused anchors are being discarded atm

if __name__ == "__main__":
    tht_filename = args.filename
    tht_role_name = args.role_name
    overwrite = args.overwrite
    tht_task_name = args.task_name

    tht_role_data = yaml_load(tht_filename)

    # TODO: This needs to be a generic recursive search generator perhaps
    tht_task_data = tht_role_data['outputs']['role_data']['value'].get(
        tht_task_name)

    new_role_task_name = tht_task_name.strip('_tasks')

    write_role_data(tht_role_name, new_role_task_name, tht_task_data)

"""
Example format of yaml to be extracted as follows

outputs:
    role_data:
        value:
            upgrade_tasks:
            .
            .
            .
            fast_forward_upgrade_tasks:
"""


"""
Example format of role layout on disk

keystone/
   tasks/
       upgrade_tasks.yaml
       fast_forward_upgrade_tasks.yaml
"""


"""
Example import to use to replace the tasks in the THT YAML

upgrade_tasks:
  - import_role:
      name: keystone
      tasks_from: upgrade.yml
"""
