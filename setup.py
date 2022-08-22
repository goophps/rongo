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
    name=meta["__name__"],
    version=meta["__version__"],
    author=meta["__author__"],
    author_email=meta["__email__"],
    description="This is not a python web framework, it's a complement to such mini frameworks like fastapi sanic. "
                "Mainly refer to Thinkphp Laravel Django Masonite.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=meta["__url__"],
    # 列出这个项目的包
    packages=[
        "rongo",
        "rongo.cache",
        "rongo.cache.drivers",
        "rongo.configuration.providers",
        "rongo.configuration",
        "rongo.container",
        "rongo.contract",
        "rongo.environment",
        "rongo.exceptions",
        "rongo.facades",
        "rongo.foundation",
        "rongo.loader",
        "rongo.providers",
        "rongo.template",
        "rongo.utils",
    ],
    # 需要额外的文件(全部罗列到MANIFEST.in文件里)
    include_package_data=True,
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
