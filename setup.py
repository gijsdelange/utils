from setuptools import setup, find_packages

setup(
    name='utils',
    version='0.0.1',
    description='general utils',
    packages = find_packages(),
    url='https://github.com/gijsdelange/utils',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Licence :: MIT Licence',
        'Topic :: Scientific/Engineering'
    ],
    license='MIT',
    install_requires=[],
    python_requires='>=2.7',
    use_2to3=False,
)