from setuptools import setup, dist

class BinaryDistribution(dist.Distribution):
    def is_pure(self):
        return False

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pyfmr",
    package_data={'pyfmr':[
        'lib/fmr-darwin-10.6-amd64.dylib',
        'lib/fmr-windows-4.0-amd64.dll',
        'lib/fmr-linux-amd64.so',
    ]},
    include_package_data=True,
    distclass=BinaryDistribution,
    version="0.0.2",
    author="Zhanliang Liu",
    author_email="liang@zliu.org",
    description="A python wrapper for FMR",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/liuzl/pyfmr",
    #packages=setuptools.find_packages(),
    packages=['pyfmr'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
