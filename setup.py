from setuptools import setup

setup(
    name='tennis_stats',
    version='1.0.0',
    author='Jad Shaheen',
    install_requires=[
        'beautifulsoup4',
        'Flask',
        'Flask-Cors',
        'guincorn',
        'requests'
    ]
)
