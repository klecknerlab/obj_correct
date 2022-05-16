from setuptools import setup

setup(
    name='obj_correct',
    version='0.1',
    description='Python-based software to compute correction lens specifications for microscope objectives.  Developed by the MUVI center at UC Merced.',
    url='https://github.com/klecknerlab/obj_correct',
    author='Dustin Kleckner',
    author_email='dkleckner@ucmerced.edu',
    license='Apache 2.0 (http://www.apache.org/licenses/LICENSE-2.0)',
    packages=['obj_correct'],
    install_requires=[ #Many of the packages are not in PyPi, so assume the user knows how to isntall them!
        # 'numpy',
        # 'PyQt5',
    ],
    # scripts=['bin/muvi_convert'],
    # entry_points={
    #     'gui_scripts': ['muvi=muvi.view.qtview:qt_viewer']
    # },
    zip_safe=False
)
