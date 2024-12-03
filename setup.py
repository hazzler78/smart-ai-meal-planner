from setuptools import setup, find_packages

setup(
    name="smart_meal_planner_backend",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "sqlalchemy",
        "pytest",
        "python-dotenv",
        "httpx",
    ],
) 