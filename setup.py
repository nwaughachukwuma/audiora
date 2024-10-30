from setuptools import find_packages, setup

setup(
    name="audiora",
    version="1.0.0",
    description="Learn or listen to anything, anytime, through the power of AI-generated audio",
    author="Chukwuma Nwaugha",
    author_email="chuks@veedo.ai",
    url="https://github.com/nwaughachukwuma/audiora",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "httpx",
        "asyncio",
        "openai",
        "anthropic",
        "pyperclip",
        "python-multipart",
        "python-slugify",
        "python-dotenv",
        "pydub",
        "firebase-admin",
        "google-auth",
        "google-cloud-storage",
        "google-api-python-client",
        "google-generativeai",
        "ruff"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
