# setup.py

from setuptools import setup, find_packages

setup(
    name="horacle",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "streamlit==1.33.0",
        "requests==2.31.0",
        "pycountry==22.3.5",
        "Pillow==10.2.0",
        "swisseph==2.10.00",
        "kerykeion==1.3.0",
        "pytz==2024.1",
        "matplotlib==3.8.3"
    ],
    extras_require={
        "dev": ["pytest==8.1.1", "pytest-mock==3.12.0"]
    },
    entry_points={
        "console_scripts": [
            "horacle=horacle.app:main"
        ]
    },
    author="Your Name",
    description="Astrology-powered chatbot and charting app using Streamlit.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Streamlit",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires=">=3.8"
)
