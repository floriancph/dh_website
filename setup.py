from setuptools import setup, find_packages

setup(
    name='webapp',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'influxdb',
        'pandas'
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
