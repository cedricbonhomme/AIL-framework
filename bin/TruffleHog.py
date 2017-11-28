#!/usr/bin/env python
# -*-coding:UTF-8 -*

import pprint
import time
from packages import Paste
from packages import lib_refine
from pubsublogger import publisher
from truffleHog import truffleHog
import re

from Helper import Process

regex = r'('
# Scheme (HTTP, HTTPS, FTP and SFTP):
regex += r'(?:(https?|s?ftp):\/\/)?'
# www:
regex += r'(?:www\.)?'
regex += r'('
# Host and domain (including ccSLD):
regex += r'(?:(?:[A-Z0-9][A-Z0-9-]{0,61}[A-Z0-9]\.)+)'
# TLD:
regex += r'([A-Z]{2,6})'
# IP Address:
regex += r'|(?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
regex += r')'
# Port:
regex += r'(?::(\d{1,5}))?'
# Query path:
regex += r'(?:(\/\S+)*)'
# Query extension for git repositories:
regex += r'(git)'
regex += r')'


find_git_repo_url_in_string = re.compile(regex, re.IGNORECASE)


def find_secrets(url):
    try:
        truffleHog.find_strings(url)
    except UnicodeEncodeError:
        print("Unicode print error")


def find_git_repo(message):
    paste = Paste.Paste(message)
    content = paste.get_p_content()

    url_git_repo = find_git_repo_url_in_string.search(content)

    if url_git_repo is not None and url_git_repo.group(0) is not None:
        print("URL parts: " + str(url_git_repo.groups()))
        print("URL: " + url_git_repo.group(0).strip())

        find_secrets(url_git_repo.group(0).strip())


if __name__ == "__main__":
    publisher.port = 6380
    publisher.channel = "Script"

    config_section = 'TruffleHog'

    p = Process(config_section)

    # Sent to the logging a description of the module
    publisher.info("Run CboModule module")

    while True:
        message = p.get_from_set()
        if message is None:
            continue

        find_git_repo(message)
