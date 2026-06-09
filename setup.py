from setuptools import setup

setup(
    name="flowin",
    version="0.1.0",
    py_modules=["main"],
    install_requires=[
        "typer>=0.12.0",
    ],
    entry_points={
        "console_scripts": [
            "flowin=main:app",
        ],
    },
)
