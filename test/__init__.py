#!/usr/bin/env python

# See Pierre's answer: <https://stackoverflow.com/a/24266885>
# on <https://stackoverflow.com/questions/1896918/running-unittest-with-
# typical-test-directory-structure>

# import the package
import infrastructure

# import the infrastructure module
from infrastructure import numpy_gcode_reader

# or an object inside the infrastructure module
from infrastructure.numpy_gcode_reader import NumpyGcodeReader
