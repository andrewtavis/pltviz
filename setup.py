import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from setuptools import find_packages

package_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(package_directory, "README.md"), encoding="utf-8") as fh:
    long_description = fh.read()

with open(os.path.join(package_directory, "requirements.txt")) as req_file:
    requirements = req_file.readlines()

setup_args = dict(
    name="pltviz",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    version="0.1.2.7",
    author="Andrew Tavis McAllister",
    author_email="andrew.t.mcallister@gmail.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    description="Standardized plots and visualizations in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="new BSD",
    url="https://github.com/andrewtavis/pltviz",
)

if __name__ == "__main__":
    setup(**setup_args)
