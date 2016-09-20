import os
import sys
from os import path
import site

python_site_packages = site.getsitepackages()[0]
python_bin_dir = [p for p in sys.path if p and p.endswith('bin')][0]
python_include_dir = path.realpath(path.join(python_bin_dir, '../include/python2.7'))


def remove_abs_path(current_path, root):
    for fn in os.listdir(current_path):
        dst = path.join(current_path, fn)
        try:
            src = os.readlink(dst)
            if not src.startswith('/'):  # already a relative path
                continue
            elif src.startswith(root):  # an absolute path inside model root
                src = path.relpath(src, dst)[3:]  # remove starting '../'
            elif src.count('local_jdk'):  # point to jvm root (not implemented)
                continue
                # src = src.replace('/usr/lib/jvm/java-8-openjdk-amd64', jdk_root)
            elif src.count('site-packages'):  # point to python site-packages directory (not implemented)
                continue
                # src = src.replace('/usr/local/lib/python2.7.12/lib/python2.7/site-packages', python_site_packages)
            elif src.count('include'):  # point to python include directory (not implemented)
                continue
                # src = src.replace('/usr/local/lib/python2.7.12/include', python_include_dir)
            else:
                continue
            print dst, '==>', src
            os.unlink(dst)
            os.symlink(src, dst)
        except:
            if path.isdir(dst):
                remove_abs_path(dst, root)

pwd = os.getcwd()
remove_abs_path(pwd, pwd)
