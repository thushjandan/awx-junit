import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='awx-junit',  
     version='1.0',
     scripts=['awx-junit'] ,
     author="Thushjandan Ponnudurai",
     author_email="thushjandan@gmail.com",
     description="A Ansible Tower or AWX utility to generate a JUnit XML report from a job.",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/thushjandan/awx-junit",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
     ],
 )
