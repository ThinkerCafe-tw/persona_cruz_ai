from setuptools import setup, find_packages
import os

# 讀取 README
with open("../../README_COMPLETE.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# 讀取 requirements
with open("../../requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="cruz-ai-sdk",
    version="1.0.0",
    author="CRUZ AI Team",
    author_email="contact@cruz-ai.example.com",
    description="多人格 AI 助手系統 Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ThinkerCafe-tw/persona_cruz_ai",
    project_urls={
        "Bug Tracker": "https://github.com/ThinkerCafe-tw/persona_cruz_ai/issues",
        "Documentation": "https://github.com/ThinkerCafe-tw/persona_cruz_ai/blob/main/README_COMPLETE.md",
        "Source Code": "https://github.com/ThinkerCafe-tw/persona_cruz_ai",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "httpx>=0.25.0",
        "websockets>=12.0",
        "pydantic>=2.0.0",
        "python-dateutil>=2.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "cruz-ai-demo=cruz_ai_sdk.demo:main",
        ],
    },
    keywords="ai artificial-intelligence chatbot personality memory cruz gemini",
)