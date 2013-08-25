# -*- coding: utf-8 -*-
import pip


def parse(config_data):
    #reqs =
    print config_data


def requirements(requirements, is_file=False):
    if is_file:
        args = ['install', '-r', requirements]
    else:
        args = ['install']
        args.extend(requirements.split())
    command = pip.main(args)