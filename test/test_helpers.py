import numpy
import unittest


from domain.commands import *


class NumpyTestHelpers(object):

    def assertNumpyArrayEquals(self,array1, array2):
        equal = numpy.array_equal(array1,array2)
        if not equal:
            self.fail("\n%s\ndid not equal\n%s" % (str(array1),str(array2)))

    def assertNumpyArrayClose(self,array1, array2):
        equal = numpy.allclose(array1,array2)
        if not equal:
            self.fail("\n%s\ndid not equal\n%s" % (str(array1),str(array2)))

class CommandTestHelpers(object):

    def almostEqual(self,a, b,tollerence = 0.0001):
        diff = a - b
        return abs(diff) < tollerence 

    def coordantesAlmostEqual(self,point_a, point_b,tollerence = 0.0001):
        return self.almostEqual(point_a[0] , point_b[0]) and self.almostEqual(point_a[1] , point_b[1])

    def assertLateralDrawEqual(self, command1, command2):
        if not self.coordantesAlmostEqual(command1.start, command2.start):
            self.fail("Command starts do not match\n%s\ndid not equal\n%s" % (command1, command2))
        if not self.coordantesAlmostEqual(command1.end,command2.end):
            self.fail("Command ends do not match\n%s\ndid not equal\n%s" % (command1, command2))
        if not self.almostEqual(command1.speed, command2.speed):
            self.fail("Command speeds do not match\n%s\ndid not equal\n%s" % (command1, command2))

    def assertLateralMoveEqual(self, command1, command2):
        self.assertLateralDrawEqual(command1, command2)

    def assertVerticleMoveEqual(self, command1, command2):
        if not (self._equal(command1.start, command2.start) and self._equal(command1.end, command2.end) and self._equal(command1.speed, command2.speed)):
            self.fail("Commands do not match\n%s\ndid not equal\n%s" % (command1, command2))

    def assertCommandEqual(self, command1, command2):
        if type(command1) != type(command2):
            self.fail("Command did not match\n%s\ndid not equal\n%s" % (str(command1), str(command2)))
        if type(command1) == LateralDraw:
            self.assertLateralDrawEqual(command1,command2)
        elif type(command1) == LateralMove:
            self.assertLateralMoveEqual(command1,command2)
        elif type(command1) == VerticalMove:
            self.assertVerticleMoveEqual(command1,command2)
        else:
            self.fail("Test Helper Unsupported type: %s" % type(command1) )

    def assertCommandsEqual(self, commands1, commands2):
        if len(commands1) != len(commands2):
            self.fail("Commands do not match\n%s\ndid not equal\n%s" % (self._stringify(commands1), self._stringify(commands2)))
        for i in range(0, len(commands1)):
            try:
                self.assertCommandEqual(commands1[i],commands2[i])
            except Exception as ex:
                self.fail("Commands do not match\n%s\ndid not equal\n%s\nDetail: %s" % (self._stringify(commands1), self._stringify(commands2), ex.message))

    def assertLayerEquals(self,layer1,layer2):
        if self.assertAlmostEqual(layer1.z, layer2.z):
            self.fail("z do not match %s did not equal %s" % (layer1.z, layer2.z))
        self.assertCommandsEqual(layer1.commands,layer2.commands)
    
    def assertLayersEquals(self,layers1,layers2):
        if len(layers1) != len(layers2):
            self.fail("Count of Layers do not match\n%s\ndid not equal\n%s" % (self._stringify(layers1), self._stringify(layers2)))
        for i in range(len(layers1)):
            self.assertLayerEquals(layers1[i],layers2[i])

    def _stringify(self,list_data):
        return [str(element) for element in list_data]

    def _equal(self,a,b, tol = 0.0001):
        return abs(a-b) <= (abs(a)+abs(b))/2 * tol

class TestHelpers(NumpyTestHelpers,CommandTestHelpers):
    def assertListDict(self,expected,actual):
        self.assertEquals(len(expected), len(actual))
        for item in expected:
            if not item in actual:
                self.fail("%s\ndid not equal\n%s\non item\n%s" % (expected,actual, item))

    def assertListContentsEqual(self,expected,actual):
        self.assertEquals(len(expected), len(actual))
        for index in range(0, len(expected)):
            self.assertEquals(str(expected[index]),str(actual[index]), '%s != %s' %(expected[index], actual[index]))