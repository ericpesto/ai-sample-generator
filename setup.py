from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="ai-wav-generator",
    version="0.1.0",
    author="Eric Petsopoulos",
    description="An AI-powered WAV generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ericpesto/ai-wav-generator",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "transformers",
        "scipy",
        "termcolor",
        "urllib3",
        "sounddevice",
        "ipython"
        # Add other dependencies here
    ],
    entry_points={
        "console_scripts": [
            "ai-wav-generator=src.main:main",  # Make sure this matches your project structure
        ],
    },
)
