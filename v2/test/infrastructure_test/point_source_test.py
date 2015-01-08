import unittest
import os
import sys
from mock import patch, MagicMock
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from infrastructure.point_source import WavFolderPointSource
from domain.point import Point


class WavFolderPointSourceTest(unittest.TestCase):
    def setUp(self):
        pass

    def default_params(self, nchannels=2, sampwidth=2, framerate=48000, nframes=4, comptype=None, compname=None):
        return (nchannels, sampwidth, framerate, nframes, comptype, compname)

    def _to_frame(self, values):
            return values.astype(np.dtype('<i2')).tostring()

    def test_init_raises_exception_if_folder_doesnt_exist(self):
        with self.assertRaises(Exception):
            WavFolderPointSource('ERRR')

    def test_init_returns_if_valid_folder(self):
        WavFolderPointSource('test_data')

    def test_init_raises_exception_if_valid_folder_but_no_wav_files(self):
        with self.assertRaises(Exception):
            WavFolderPointSource('.')

    @patch('infrastructure.point_source.wave')
    def test_get_points_raises_exception_given_non_stereo_wav_file(self, mock_wave):
        wave_file=MagicMock()
        mock_wave.open.return_value = wave_file
        wave_file.getparams.return_value(self.default_params(nchannels=1))
        wfps = WavFolderPointSource('test_data')
        with self.assertRaises(Exception):
            points = wfps.get_points()
            points.next()
        mock_wave.open.assert_called_with('layer_69.88_.wav', 'r')

    @patch('infrastructure.point_source.wave.open')
    @patch.object(os, 'listdir')
    def test_get_points_returns_expected_point(self, mock_listdir, mock_open):
        mock_listdir.return_value = ['BLA_1.0_.wav']
        mock_wave = MagicMock()
        mock_open.return_value = mock_wave
        mock_wave.getparams.return_value = self.default_params(nframes=4)
        l = np.array((-32768, 0, 32767, 0))
        data = np.column_stack((l, l))
        wave_data = data.astype(np.dtype('<i2')).tostring()
        mock_wave.getnframes.return_value = wave_data
        wfps = WavFolderPointSource('test_data')
        expected_point = Point(1.0, 1.0, 1.0, True)

        points = list(wfps.get_points())

        self.assertEquals(1, len(points))
        self.assertEqual(expected_point, points[0])

    @patch('infrastructure.point_source.wave.open')
    @patch.object(os, 'listdir')
    def test_get_points_returns_expected_points(self, mock_listdir, mock_open):
        mock_listdir.return_value = ['BLA_1.0_.wav']
        mock_wave = MagicMock()
        mock_open.return_value = mock_wave
        mock_wave.getparams.return_value = self.default_params(nframes=8)
        l = np.array((-32768, 0, 32767, 0, -32768, 0, 32767, 0))
        data = np.column_stack((l, l))
        wave_data = data.astype(np.dtype('<i2')).tostring()
        mock_wave.getnframes.return_value = wave_data
        wfps = WavFolderPointSource('test_data')
        expected_point = Point(1.0, 1.0, 1.0, True)

        points = list(wfps.get_points())

        self.assertEquals(2, len(points))
        self.assertEqual(expected_point, points[0])
        self.assertEqual(expected_point, points[1])

    @patch('infrastructure.point_source.wave.open')
    @patch.object(os, 'listdir')
    def test_get_points_returns_expected_points_with_minimum_value(self, mock_listdir, mock_open):
        mock_listdir.return_value = ['BLA_1.0_.wav']
        mock_wave = MagicMock()
        mock_open.return_value = mock_wave
        mock_wave.getparams.return_value = self.default_params(nframes=8)
        l = np.array((-32768, 0, 32767, 0, -32768, 0, 8192, 0))
        data = np.column_stack((l, l))
        wave_data = data.astype(np.dtype('<i2')).tostring()
        mock_wave.getnframes.return_value = wave_data
        wfps = WavFolderPointSource('test_data')
        expected_point1 = Point(1.0, 1.0, 1.0, True)
        expected_point2 = Point(-1.0, -1.0, 1.0, True)

        points = list(wfps.get_points())

        self.assertEquals(2, len(points))
        self.assertEqual(expected_point1, points[0])
        self.assertEqual(expected_point2, points[1])

    @patch('infrastructure.point_source.wave.open')
    @patch.object(os, 'listdir')
    def test_get_points_returns_expected_points_for_many_files(self, mock_listdir, mock_open):
        mock_listdir.return_value = ['BLA_1.0_.wav', 'BLA_1.1_.wav']
        mock_wave = MagicMock()
        mock_open.return_value = mock_wave
        mock_wave.getparams.return_value = self.default_params(nframes=4)
        l = np.array((-32768, 0, 32767, 0))
        data = np.column_stack((l, l))
        wave_data = data.astype(np.dtype('<i2')).tostring()
        mock_wave.getnframes.return_value = wave_data
        wfps = WavFolderPointSource('test_data')
        expected_point1 = Point(1.0, 1.0, 1.0, True)
        expected_point2 = Point(1.0, 1.0, 1.1, True)

        points = list(wfps.get_points())

        self.assertEquals(2, len(points))
        self.assertEqual(expected_point1, points[0])
        self.assertEqual(expected_point2, points[1])

    @patch('infrastructure.point_source.wave.open')
    @patch.object(os, 'listdir')
    def test_get_points_returns_expected_points_for_many_files_in_order(self, mock_listdir, mock_open):
        mock_listdir.return_value = ['BLA_1.1_.wav', 'BLA_1.0_.wav', 'BLA_1.2_.wav']
        mock_wave = MagicMock()
        mock_open.return_value = mock_wave
        mock_wave.getparams.return_value = self.default_params(nframes=4)
        l = np.array((-32768, 0, 32767, 0))
        data = np.column_stack((l, l))
        wave_data = data.astype(np.dtype('<i2')).tostring()
        mock_wave.getnframes.return_value = wave_data
        wfps = WavFolderPointSource('test_data')
        expected_point1 = Point(1.0, 1.0, 1.0, True)
        expected_point2 = Point(1.0, 1.0, 1.1, True)
        expected_point3 = Point(1.0, 1.0, 1.2, True)

        points = list(wfps.get_points())

        self.assertEquals(3, len(points))
        self.assertEqual(expected_point1, points[0])
        self.assertEqual(expected_point2, points[1])
        self.assertEqual(expected_point3, points[2])


if __name__ == '__main__':
    unittest.main()
