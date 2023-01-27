from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in tuna_technology/__init__.py
from tuna_technology import __version__ as version

setup(
	name="tuna_technology",
	version=version,
	description="Tuna Technology",
	author="tuna-technology",
	author_email="tuna-technology@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
