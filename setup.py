try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from setuptools import find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup_args = dict(
    name='stdviz',
    version='0.0.1.1',
    description='Standardized vizualization in Python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_namespace_packages(),
    license='new BSD',
    url="https://github.com/andrewtavis/stdviz",
    author='Andrew Tavis McAllister',
    author_email='andrew.t.mcallister@gmail.com'
)

install_requires = [
    'numpy',
    'scipy',
    'pandas',
    'matplotlib',
    'seaborn',
    'colormath'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)