from setuptools import setup, find_packages

setup(
    name="InvCon",
    description="A Dynamic Invariant Detector for Ethereum Smart Contracts",
    url="https://github.com/Franklinliu/InvCon-tool",
    author="Liu Ye",
    version="0.1.0",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "solc-select",
        "requests",
        "beautifulsoup4",
        "pandas",
        "cloudscraper",
        "alive-progress",
        "web3",
    ],
    # dependency_links=["git+https://github.com/crytic/crytic-compile.git@master#egg=crytic-compile"],
    license="AGPL-3.0",
    long_description=open("README.md").read(),
    entry_points={
        "console_scripts": [
            "invcon = invcon.__main__:main"
        ]
    },
)
