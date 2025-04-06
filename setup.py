from setuptools import setup, find_packages

setup(
    name="ExplicitUtil",
    version="1.3",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "tqdm",
        "namer",
        "pillow",
    ],
    author="Alchemist-Aloha",
    description="A utility library for managing media files",
    url="https://github.com/Alchemist-Aloha/explicit_util",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
