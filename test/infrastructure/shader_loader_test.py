import unittest
import os
import sys
from mock import patch, mock_open
import OpenGL.GLUT as glut
import OpenGL.GL as gl

scriptDir = os.path.dirname(os.path.realpath(__file__))
testDir = os.path.dirname(scriptDir)
assert(os.path.isfile(os.path.join(testDir, "tests.py")))
repoDir = os.path.dirname(testDir)
infrDir = os.path.join(repoDir, 'infrastructure')
testInfrDir = os.path.join(testDir, 'infrastructure')
print("[shader_loaded_test.py]")
print("scriptDir: %s" % scriptDir)
assert(os.path.isdir(scriptDir))
# sys.path.insert(0, scriptDir)
print("testDir: %s" % testDir)
assert(os.path.isdir(testDir))
sys.path.insert(0, testDir)
# ^ It has a copy of infrastructure with tests not infrastructure.

print("repoDir: %s" % repoDir)
assert(os.path.isdir(repoDir))
sys.path.insert(0, repoDir)
# ^ it needs the real infrastructure module in order to import
#   numpy_gcode_reader

print("infrDir: %s" % infrDir)
assert(os.path.isdir(infrDir))
badInfrFile = os.path.join(infrDir, "shader_loader_test.py")
testInfrFile = os.path.join(testInfrDir, "shader_loader_test.py")
assert(not os.path.isfile(badInfrFile))
assert(os.path.isfile(testInfrFile))
# sys.path.insert(0, infrDir)

print("cwd: %s" % os.getcwd())
print("")
print("path:")
for path in sys.path:
    print("  - " + path)
print("")
from infrastructure.shader_loader import ShaderLoader


class ShaderLoaderTest(unittest.TestCase):
    def setUp(self):
        glut.glutInit()
        glut.glutInitDisplayMode(glut.GLUT_RGBA | glut.GLUT_DOUBLE | glut.GLUT_DEPTH)
        glut.glutInitWindowSize(20, 20)
        self.window_id = glut.glutCreateWindow(self.__class__.__name__)
        self.test_data_path = os.path.join(scriptDir, 'test_data')

    def tearDown(self):
        glut.glutDestroyWindow(self.window_id)

    def test_load_shaders_reads_and_creates_shaders(self):
        result = ShaderLoader.load_shaders(
            os.path.join(self.test_data_path, 'good_vertex.glsl'),
            os.path.join(self.test_data_path, 'good_fragment.glsl')
        )
        self.assertTrue(result)



if __name__ == '__main__':
    unittest.main()
