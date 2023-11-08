# openai-sandbox

## virtual environment

make sure the `openai-env` virtual environment is loaded and running. to load, on the command line in the root of the repo do `python -m venv openai-env`; to run, on the command line (in macOS) do `source openai-env/bin/activate`.


## API key

as of initialization, this has a `.env` file with a line like `OPENAI_API_KEY=asd123`. however, i actually saved the key in the virtual environment's environmental variables, by putting a line like `export OPENAI_API_KEY='asd123'` at the end of the file `openai-env/bin/activate`.
