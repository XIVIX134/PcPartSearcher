from setuptools import setup, find_packages

setup(
    name="pc-part-searcher",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'flask',
        'flask-cors',
        'requests',
        'beautifulsoup4',
        'aiohttp'
    ]
)
