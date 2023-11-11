# sleep-stories

## setup

### venv

make sure the `openai-env` virtual environment is both loaded and running. to load, on the command line in the root of the repo do `python -m venv openai-env`; to run, on the command line (in macOS) do `source openai-env/bin/activate`.

### openai module

make sure to do `pip install openai`. (i think `pip` only exists once python is installed (e.g. because usually i do `pip3` when i only have `python3` and `pip` doesn't even work). so, be sure to do this _after_ the venv setup above.)

### API key

this ought to have an API key saved (say at the bottom of the file `openai-env/bin/activate`), as explained [here](https://platform.openai.com/docs/quickstart/step-2-setup-your-api-key). remember that a terminal window sets the environment variables right when it's opened, so if/when this is updated, open a _new_ terminal window to test the new settings.