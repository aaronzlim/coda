import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="coda", # Replace with your own username
    version="0.0.1",
    author="Aaron Lim",
    author_email="aaronzlim@gmail.com",
    description="CoxOrb Data Analyzer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aaronzlim/coda",
    project_urls={
        "Bug Tracker": "https://github.com/aaronzlim/coda/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(where="src"),
    install_requires=[
        "matplotlib==3.4.2",
        "pysimplegui==4.40.0",
        "pytz==2021.1",
    ],
    entry_points={"console_scripts": ["coda=src.__main__:main"]},
    python_requires=">=3.8",
)