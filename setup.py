import setuptools # type: ignore

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tosclib",
    version="0.3.5",
    author="Alberto Valdez",
    author_email="avq5ac1@gmail.com",
    description="Generate and edit Touch OSC .tosc files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AlbertoV5/tosclib",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    package_data={"tosclib": ["py.typed"]},
    python_requires=">=3.10",
    install_requires=[
        "lxml>=4.9.0",
        "numpy>=1.22.3"
    ]
)