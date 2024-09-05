from setuptools import setup, find_packages

setup(
    name="groc-edit",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "opencv-python>=4.5.5.64",
        "dlib==19.24.2",
        "numpy==1.23.5"
    ],
    author="Taehyun Jung",
    author_email="taehyun.jung@monolith.co.kr",
    description="A tool for cropping and resizing portrait images based on face detection",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/monolith-taehyun/groc-edit",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)