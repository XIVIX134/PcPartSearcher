from setuptools import setup, find_packages

setup(
    name="pc-part-searcher",
    version="0.1",
    packages=find_packages(include=['app*', 'scrapers*']),
    install_requires=[
        'fastapi',
        'uvicorn',
        'requests',
        'beautifulsoup4',
        'aiohttp',
        'httpx',
        'asyncio'
    ]
)
