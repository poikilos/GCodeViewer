import unittest
import os
import sys
print("[tests.py]")

scriptDir = os.path.dirname(os.path.realpath(__file__))
if len(scriptDir) < 1:
    print("ERROR: couldn't get os.path.dirname of script file \"%s\""
          % __file__)
testDir = scriptDir  # same since we're in test
assert(os.path.isfile(os.path.join(testDir, "tests.py")))
repoDir = os.path.dirname(testDir)
infrDir = os.path.join(repoDir, 'infrastructure')
testInfrDir = os.path.join(testDir, 'infrastructure')
print("repoDir: %s" % repoDir)
print("infrDir: %s" % infrDir)
print("testInfrDir: %s" % testInfrDir)
assert(os.path.isdir(infrDir))
badInfrFile = os.path.join(infrDir, "shader_loader_test.py")
testInfrFile = os.path.join(testInfrDir, "shader_loader_test.py")
assert(not os.path.isfile(badInfrFile))
assert(os.path.isfile(testInfrFile))

sys.path.insert(0, repoDir)
sys.path.insert(0, testDir)
# ^ testDir is top priority since contains a test version of
#   infrastructure.
print("[tests.py] Test path: \"%s\"" % testDir)

loader = unittest.TestLoader()
suite = loader.discover(testDir, pattern='*test.py')

# sys.path.insert(0, repoDir)
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)

problems = len(result.errors) + len(result.failures)
print("\nProblems: %s\n" % problems)
exit(problems)
