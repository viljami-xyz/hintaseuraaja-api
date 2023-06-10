"""
    Setup script to install current package to virtualenv
    
    Locate the current virtual environment and find its site-packages folder
    Write the current package location to a .pth file in the site-packages folder
    so it can be imported from anywhere in the virtual environment
"""

import os
import sys
import site
from setuptools import setup, find_packages

PACKAGE_NAME = "hintascraper"
VERSION = "0.1.0"
PACKAGE_LOCATION = os.path.dirname(os.path.abspath(__file__))
VENV_SP_LOC = site.getsitepackages()[-1]

EXTRAS = {}
REQUIRES = []
with open("requirements.txt", encoding="UTF-8") as f:
    for line in f:
        line, _, _ = line.partition("#")
        line = line.strip()
        if ";" in line:
            requirement, _, specifier = line.partition(";")
            for_specifier = EXTRAS.setdefault(f":{specifier}", [])
            for_specifier.append(requirement)
        else:
            if "@" in line:
                line = line.replace(" @ ", "@")
            REQUIRES.append(line)

if os.getenv("VIRTUAL_ENV") and "develop" in sys.argv:
    if not "site-packages" in VENV_SP_LOC:
        raise ValueError("Could not find site-packages folder")

    with open(
        os.path.join(VENV_SP_LOC, f"{PACKAGE_NAME}.pth"), "w", encoding="UTF-8"
    ) as open_file:
        open_file.write(PACKAGE_LOCATION)

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    packages=find_packages(),
    install_requires=REQUIRES,
    package_data={PACKAGE_NAME: []},
)
