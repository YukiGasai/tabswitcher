from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        # put your post-install command here
        subprocess.call(['bt', 'install'], shell=True)
        print('Install the BroTab extension and restart your browser to use tabswitcher.')

setup(
    name='tabswitcher',
    version='0.1',
    packages=find_packages(),
    description="A tool for efficient browser tab switching outside the browser",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='YukiGasai',
    author_email='r.lindede@googlemail.com',
    url='https://github.com/YukiGasai/tabswitcher',
    entry_points={
        'console_scripts': [
            'tabswitcher=src.__init__:main',
        ],
    },
    cmdclass={
        'install': PostInstallCommand,
    },
    license='AGPL-3.0',
    classifiers=[],
    keywords='tabswitcher, browsertool, tool',
    install_requires=[
        'chardet',
        'fuzzywuzzy',
        'psutil',
        'PyQt5',
        'schedule',
        'brotab',
        'werkzeug<3.0',
    ],
)