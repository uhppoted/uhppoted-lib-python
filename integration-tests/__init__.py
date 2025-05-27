# pylint: disable=invalid-name
"""
Sets path for local imports.
"""

import os
import sys

PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(PROJECT_PATH, "src")

sys.path.append(SOURCE_PATH)
