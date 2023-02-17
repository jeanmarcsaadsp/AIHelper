# AI Helper

## Overview
This CLI tool communicates with OpenAI's Codex Model to do a number of code completion tasks.

## Installation
In order to install the tool as a CLI application, you can execute the following from the root directory
```
pip install -r requirements.txt
python setup.py sdist bdist_wheel
pip install .
```

## Features
### Unit Test Generation
AI Helper can, given an input class, generate a working test suite file in the test framework of your choice.

Usage:
```
export OPENAI_API_KEY="sk-xxx.."
aihelper examples/calculator.php --test-framework phpunit --output-dir ./
```