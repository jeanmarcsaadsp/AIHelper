import os
import openai
import click
from jinja2 import Environment, FileSystemLoader
from enum import Enum

openai.api_key = os.getenv("OPENAI_API_KEY")

class FileType(Enum):
    PYTHON = 'py'
    TYPESCRIPT = 'ts'
    JAVASCRIPT = 'js'
    PHP = 'php'

def get_language_from_extension(extension):
    for file_type in FileType:
        if file_type.value == extension:
            return file_type.name
    raise ValueError('Unsupported file extension: {}'.format(extension))

def detect_file_type(file_path):
    """Detects the file type based on its extension."""
    _, extension = os.path.splitext(file_path)
    if extension == f'.{FileType.PYTHON.value}':
        return FileType.PYTHON.value
    elif extension == f'.{FileType.TYPESCRIPT.value}':
        return FileType.TYPESCRIPT.value
    elif extension == f'.{FileType.JAVASCRIPT.value}':
        return FileType.JAVASCRIPT.value
    elif extension == f'.{FileType.PHP.value}':
        return FileType.PHP.value
    else:
        raise ValueError(f'Unsupported file type: {extension}')

def generate_unit_tests(language, test_framework, code, progress):
  environment = Environment(loader=FileSystemLoader("./templates"))
  template = environment.get_template("prompt-generate-unit-tests.txt")
  progress.update(10)

  prompt = template.render(
      test_framework = test_framework,
      language = language,
      code_raw = code
  )

  progress.update(35)

  response = openai.Completion.create(
    model="text-davinci-003",
    prompt= prompt,
    max_tokens=2048
  )

  progress.update(60)

  if not response.choices:
      raise ValueError('No unit tests generated')
  return response['choices'][0]['text']

@click.group()
def cli():
    pass

@click.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--test-framework', default='unittest', help='Test framework to use (default: unittest)')
@click.option('--output-dir', default='.', help='Output directory for generated unit tests (default: current directory)')
def generate_tests(file, test_framework, output_dir):
    """Generates unit tests using OpenAI's Codex API."""
    if not os.getenv("OPENAI_API_KEY"):
        click.echo('OPENAI_API_KEY Environment Variable is not set!')
        return
    with open(file, 'r') as f:
        code = f.read()
    try:
        file_type = detect_file_type(file)
    except ValueError as e:
        click.echo(str(e))
        return
    try:
        language = get_language_from_extension(file_type)
        click.echo("Generating unit tests using OpenAI's Davinci Codex V3...")
        click.echo(f"Input File: {file}")
        click.echo(f"Language: {language}")
        click.echo(f"Test Framework: {test_framework}")
        with click.progressbar(length=100) as progress:
            unit_tests = generate_unit_tests(language, test_framework, code, progress)
            progress.update(100)
    except ValueError as e:
        click.echo(str(e))
        return
    output_file = os.path.join(output_dir, f'{os.path.splitext(os.path.basename(file))[0]}_test.{file_type}')
    with open(output_file, 'w') as f:
        f.write(unit_tests)
    click.echo(f'Unit tests written to {output_file}')

cli.add_command(generate_tests)

if __name__ == '__main__':
    cli()