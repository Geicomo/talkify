from setuptools import setup, find_packages

setup(
    name='Talkify',  # Name of your project
    version='0.1.0',  # Version of your project
    packages=find_packages(),  # Automatically find packages in the project
    py_modules=['speech_to_text'],  # List your main script here
    include_package_data=True,  # Include additional files specified in MANIFEST.in or package data
    install_requires=[
        'certifi==2024.7.4',
        'charset-normalizer==3.3.2',
        'comtypes==1.4.5',
        'fuzzywuzzy==0.18.0',
        'idna==3.7',
        'Levenshtein==0.25.1',
        'PyAudio==0.2.14',
        'pygame==2.6.0',
        'pypiwin32==223',
        'pyttsx3==2.90',
        'pywin32==306',
        'rapidfuzz==3.9.4',
        'redis==5.0.7',
        'requests==2.32.3',
        'setuptools==71.1.0',
        'SpeechRecognition==3.10.4',
        'spotipy==2.24.0',
        'typing_extensions==4.12.2',
        'urllib3==2.2.2',
    ],
    entry_points={
        'console_scripts': [
            'speech_to_text=speech_to_text:main',  # Command-line tool entry point
        ],
    },
    description='A speech-to-text application using various Python libraries.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Geicomo/talkify',  # Your project's URL
    author='Geicomo',
    author_email='geicomoservices@gmail.com',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify the Python versions your project supports
)
