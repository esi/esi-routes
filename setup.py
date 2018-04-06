"""EVE Swagger Interface - Endpoint."""


from setuptools import setup, find_packages
from setuphelpers import long_description, git_version, test_command


setup(
    name="esi-routes",
    version=git_version(),
    description="EVE Swagger Interface Endpoint - esi-routes",
    long_description=long_description(),
    cmdclass=test_command(),
    packages=find_packages(),
    author="",
    author_email="",
    url="",
    install_requires=["esi >= 0.8.0", "fibonacci-heap-mod"],
    extras_require={"generate": ["bravado"]},
    package_data={"esi_routes": ["jumpmap.json"]},
    include_package_data=True,
    zip_safe=False,
    setup_requires=["setuphelpers"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Flask",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
    ],
)
