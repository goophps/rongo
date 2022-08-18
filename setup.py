import setuptools
import os
meta = {}
with open(
    os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "rongo", "__init__.py"
    ),
    "r",
) as f:
    exec(f.read(), meta)

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="rongo",
    version=meta["__version__"],
    author="randolph",
    author_email="goophps@gmail.com",
    description="This is not a python web framework, it's a complement to such mini frameworks like fastapi sanic. Mainly refer to Thinkphp Laravel Django Masonite.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/goophps/rongo.git",
    # 列出这个项目的包
    packages=[
      "rongo",
      "rongo.cache.drivers",
      "rongo.cache",
      "rongo.utils",
    ],
    # 依赖的包，将自动安装
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
