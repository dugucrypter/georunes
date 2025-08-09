from setuptools import setup, find_packages

setup(
    packages=find_packages(include=['georunes*'], ),
    python_requires=">=3.6",
    install_requires=["matplotlib",
                      "numpy",
                      "scipy",
                      "pandas",
                      "python-ternary",
                      "xlsxwriter"],
    include_package_data=True,
    package_data={"georunes": ["data/*.txt", "data/*.csv"]}
)
