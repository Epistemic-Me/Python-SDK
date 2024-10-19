from setuptools import setup, find_packages

setup(
    name="epistemic_me",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'epistemic_me': ['generated/proto/**/*.py'],
    },
    install_requires=[
        "grpcio",
        "protobuf",
        "google-api-python-client",
    ],
    extras_require={
        "dev": [
            "pytest",
            "mypy",
            "black",
            "isort",
            "grpcio-tools",
        ],
    },
)
