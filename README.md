# GCodeViewer

## Use
```
python gcodeviewer.py -c
```

## Install
### Windows
- install Python 3
- install pyopengl for Python 3
- install wxpython for Python 3

### Linux

#### RPM-based (Fedora, possibly CentOS, RockyLinux or others)
```
sudo dnf -y install python3-wxpython4 python3-pyopengl
```

### DEB-based (Ubuntu, Debian)
See <https://askubuntu.com/questions/974287/how-to-import-wx-on-ubuntu-16-04>.
```
# Python 2 (not known to work with this software):
sudo apt install -y python-wxgtk3.0 python-wxgtk3.0-dev python-opengl python-numpy python-pillow
# Python 3:
sudo apt install -y python3-wxgtk4.0 python3-numpy python3-opengl
```

#### Non-packaged
```
# or see https://stackoverflow.com/questions/11215362/importerror-no-module-named-opengl-gl
# sudo easy_install pyopengl
# or:
# python3 -m pip install --user pyopengl
```

#### For Testing (DEB-based)
```
# Python2
sudo apt install python-mock
# Python3
sudo apt install python3-mock
```
