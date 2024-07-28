from setuptools import setup, find_packages

setup(
    name='Talkify',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
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
        'python-Levenshtein==0.25.1',
        'pyttsx3==2.90',
        'pywin32==306',
        'rapidfuzz==3.9.4',
        'redis==5.0.7',
        'requests==2.32.3',
        'setuptools==71.1.0',
        'SpeechRecognition==3.10.4',
        'spotipy==2.24.0',
        'typing_extensions==4.12.2',
        'urllib3>=1.0,<2.0',  # Assuming you want the latest 1.x version
    ],
    entry_points={
        'console_scripts': [
            'talkify=talkify.main:main',
        ],
    },
    description='A Speech to text program for controlling Spotify',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Geicomo/Talkify',
    author='Geicomo',
    author_email='geicomoservices@gmail.com',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
