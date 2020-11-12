import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cavaliercontours-python",
    version="0.0.1",
    author="Lucas Felix",
    author_email="lucas.felix0738@gmail.com",
    description="Python binding to the CavalierContours C++ library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/proto3/cavaliercontours-python",
    packages=setuptools.find_packages(),
    package_data={'cavaliercontours': ['lib/libCavalierContours.so']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
    ],
)
