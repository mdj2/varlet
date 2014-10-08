# Varlet

Varlet lets you prompt for variables at runtime, and saves them to a variables.yaml file.

## Install

    pip install varlet

## Usage

In your settings.py file add:

```python
from varlet import variable
```

whenever you declare a variable that could change depending on the environment,
use:

```python
# It is OK to make this True if you are in dev
DEBUG = variable("DEBUG", default=False)
```

If this "DEBUG" variable is not defined in variables.yaml, the user is prompted
to enter a Python expression to set it. Otherwise, it is read from
variables.yaml.

When the prompt is displayed, the comments directly above the call to
`variable()` are displayed, and the prompt has a default value as specified by
the `default` argument.


## Implementation Details

The first module to make a call to `variable()` determines the location of the
variables.yaml file. Varlet will look in the directory that the calling module is
located in. If variables.yaml does not exist in that directory, it is created
there.

If STDIN is not a tty-like interface, then a KeyError is raise if the varable
is not set in variables.yaml.
