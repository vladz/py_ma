from setuptools import setup, find_packages

setup(
    name='py_ma',
    version='0.0.0',
    packages=['py_ma'],
    author='VZ',
    install_requires=[
        'marshmallow==3.0.0b9',
        'xmltodict==0.11.0'
    ],
    python_requires='>=3.7',
    extras_require={
        'dev': ['pytest']
    },
    include_package_data=True,
    setup_requires=['pytest-runner==4.2'],
    tests_require=['pytest'],
    zip_safe=False
)
