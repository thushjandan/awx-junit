import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="awx-junit",
    version="1.1",
    entry_points={"console_scripts": ["awx-junit=awx_junit.awx_junit:main"]},
    author="Thushjandan Ponnudurai",
    author_email="thushjandan@gmail.com",
    description=(
        "A Ansible Tower or AWX utility " "to generate a JUnit XML report from a job."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/thushjandan/awx-junit",
    packages=setuptools.find_packages(),
    install_requires=[
        "junit-xml",
    ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Testing",
    ],
)
