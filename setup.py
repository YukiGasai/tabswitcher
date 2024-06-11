from setuptools import setup

setup(
    name='tabswitcher',
    version='0.1.11',
    packages=['tabswitcher'],
    package_dir={'tabswitcher': 'src/tabswitcher'},
    package_data={'tabswitcher': ['assets/*']},
    description="A tool for efficient browser tab switching outside the browser",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='YukiGasai',
    author_email='r.lindede@googlemail.com',
    url='https://github.com/YukiGasai/tabswitcher',
    entry_points={
        'console_scripts': [
            'tabswitcher=tabswitcher.__main__:main',
        ],
    },
    license='AGPL-3.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    keywords='tabswitcher, browsertool, tool',
    install_requires=[
        'werkzeug<3.0', # werkzeug 3.0 breaks flask and by extension brotab
        'fuzzyfinder',
        'PyQt5',
        'schedule',
        'pynput;platform_system=="Windows"',
        'pywin32;platform_system=="Windows"',
        'pyWinhook;platform_system=="Windows"',
    ],
)