import os
from setuptools import setup

# passwheel
# A password and secret personal storage tool.


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="passwheel",
    version="0.3.0",
    description="A password and secret personal storage tool.",
    author="Johan Nestaas",
    author_email="johannestaas@gmail.com",
    license="GPLv3",
    keywords="password storage crypto",
    url="https://bitbucket.org/johannestaas/passwheel",
    packages=['passwheel'],
    package_dir={'passwheel': 'passwheel'},
    long_description=read('README.rst'),
    classifiers=[
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Environment :: X11 Applications :: Qt',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
    ],
    install_requires=[
        'pynacl',
        'colorama',
        'fuzzywuzzy[speedup]',
    ],
    entry_points={
        'console_scripts': [
            'passwheel=passwheel:main',
        ],
    },
    # If you get errors running setup.py install:
    # zip_safe=False,
    #
    # For including non-python files:
    # package_data={
    #     'passwheel': ['templates/*.html'],
    # },
    # include_package_data=True,
)
