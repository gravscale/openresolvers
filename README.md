# OpenResolvers

## Description

The `openresolvers.py` script is designed to find open DNS resolvers within specified network blocks. It employs asynchronous Python and provides a variety of options for fine-grained control over the discovery process.

## Usage

The script's usage details can be seen by running `openresolvers.py -h`. Below is the output of the help command:

```
usage: openresolvers.py [-h] [-v] [-o OUTPUT] [-l LOGFILE] [-a] [-q] [-se] [-so] [-sc] [--version] networks [networks ...]

Find open resolvers

positional arguments:
networks Network blocks in CIDR format

optional arguments:
-h, --help show this help message and exit
-v, --verbose
-o OUTPUT, --output OUTPUT
Output CSV file
-l LOGFILE, --logfile LOGFILE
-a, --auto_close Auto close curses
-q, --quiet No curses display
-se, --show_errors
-so, --show_open
-sc, --show_closed
--version show program's version number and exit
```


## Installation

### Requirements

- Python 3.7 or higher
- aiodns
- curses

### Steps 

1. Clone this repository.
2. Install the requirements using pip
3. Run the script with desired options.


### Optional: Using Virtual Environment

If you prefer to use a virtual environment to manage dependencies, you can do the following:

1. Install `virtualenv` if you haven't.
2. Create a virtual environment.

```
virtualenv env
```

3. Activate the virtual environment.
- On macOS and Linux:
```
source env/bin/activate
```
- On Windows:
```
.\env\Scripts\activate
```
4. Install the requirements within the virtual environment.

```
pip install -r requirements.txt
```

To deactivate the virtual environment, simply run:
```
deactivate
```

## Usage

Run the script with desired options. For more details, see the [Usage](#usage) section.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

