import setuptools

requirements = ['PyYaml']

with open("README.md", 'r', encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name='formair',
    version='1.3.1',
    author='K8sCat',
    author_email='k8scat@gmail.com',
    description='auto Forward eMails with custom Rules',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/k8scat/ForMaiR',
    packages=setuptools.find_packages(),
    entry_points={'console_scripts': ['formair = formair.formair:main']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    python_requires='>=3.6',
)