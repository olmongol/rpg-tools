#!/usr/bin/env python3
import subprocess

tag = subprocess.check_output(["git", "describe", "--tags", "--abbrev=0"]).decode('UTF-8').strip('\n')
date = subprocess.check_output(["git", "log", "-1", "--format=%cd"]).decode('UTF-8').strip('\n')
print(f"Version: {tag} Build: {date}")
