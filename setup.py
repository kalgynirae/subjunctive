from setuptools import setup

setup(
    name='subjunctive',
    version='0.1',
    packages=['subjunctive'],
    install_requires=[
        'pyglet ==1.2alpha1',
    ],
    dependency_links=[
        'hg+https://code.google.com/p/pyglet/#egg=pyglet-1.2alpha1',
    ],
)
