from setuptools import setup, find_packages

setup(
    name='ethereum-arbitrage-bot',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'web3',
        # other dependencies...
    ],
    entry_points={
        'console_scripts': [
            'find-arbitrage-opportunity = scripts.find_arbitrage_opportunity:main',
            # other scripts...
        ],
    },
)
