import unittest
import os
import sys
try:
    from StringIO import StringIO
except ImportError:
    # Python 3
    # print("* using Python 3 io")
    from io import StringIO
import time

scriptDir = os.path.dirname(os.path.realpath(__file__))
repoDir = os.path.dirname(scriptDir)
testDir = os.path.join(repoDir, "test")
assert(os.path.isdir(os.path.join(testDir, "test_data")))

from infrastructure.numpy_gcode_reader import NumpyGcodeReader


class NumpyGcodeReaderTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_run_starts_run_loop_and_cancel(self):
        gcode_line = "G01 X0.00 Y0.00 E1 F100.0\n"
        test_gcode = StringIO(gcode_line * 100000)
        npgcr = NumpyGcodeReader(test_gcode)
        npgcr.start()
        self.assertEquals("Running", npgcr.state)
        npgcr.close()
        self.assertEquals("Aborted", npgcr.state)

    def test_run_starts_run_loop_and_complete(self):
        gcode_line = "G01 X0.00 Y0.00 E1 F100.0\n"
        test_gcode = StringIO(gcode_line)
        npgcr = NumpyGcodeReader(test_gcode)
        npgcr.start()
        time.sleep(0.1)
        self.assertEquals("Complete", npgcr.state)

    def test_get_current_should_return_state_and_arrays_of_points(self):
        gcode_line = "G01 X0.00 Y1.00 E1 F100.0\n"
        test_gcode = StringIO(gcode_line)
        npgcr = NumpyGcodeReader(test_gcode)
        npgcr.start()
        time.sleep(0.1)
        results = npgcr.get_current()

        self.assertEquals("Complete", results["State"])
        self.assertEquals([[0.0, 0.0, 0.0, 1.0], [0.0, 1.0, 0.0, 1.0]], results["Points"])
        self.assertEquals([[0.0, 1.0, 0.0, 1.0], [0.0, 1.0, 0.0, 1.0]], results["Colors"])


if __name__ == '__main__':
    unittest.main()
