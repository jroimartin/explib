import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="explib",
    version="0.0.1",
    author="Roi Martin",
    author_email="jroi.martin@gmail.com",
    description="Python package for CTFs and exploit development.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jroimartin/explib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
