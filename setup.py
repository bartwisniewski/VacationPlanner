import setuptools

test_deps = [
    "daphne==4.0.0",
    "pytest==7.2.0",
    "mock==4.0.3",
    "parse==1.19.0",
    "psutil==5.9.1",
    "pynmea2==1.18.0",
    "pyserial==3.5",
    "requests==2.28.1",
    "requests-mock==1.9.3",
    "watchdog==2.1.9",
    "parameterized==0.8.1",
    "Django==4.1.3",
    "django-storages==1.13.2",
    "djangorestframework==3.14.0",
]

libs = {"test": test_deps}

setuptools.setup(
    name="d-box-firmware",
    version="3.5",
    description="D-box firmware for dairy haulers",
    url="https://gitlab.com/bettersolutions/d-box/d-box-firmware/d-box-firmware",
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    extras_require=libs,
    classifiers=[
        "Programming Language :: Python :: 3.10",
    ],
)
