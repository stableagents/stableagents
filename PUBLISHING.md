# Publishing stableagents-ai to PyPI

Follow these steps to publish the package to PyPI:

## 1. Create a PyPI Account

If you don't already have one, create an account at [PyPI](https://pypi.org/account/register/).

## 2. Generate an API Token

1. Log in to PyPI
2. Go to Account Settings → API tokens
3. Create a new API token with scope "Entire account" or limited to the stableagents-ai project

## 3. Configure Poetry with your API Token

Run the following command, replacing `YOUR_API_TOKEN` with the token you generated:

```bash
poetry config pypi-token.pypi YOUR_API_TOKEN
```

## 4. Publish the Package

Now you can publish the package to PyPI with:

```bash
poetry publish
```

Or to build and publish in one step:

```bash
poetry publish --build
```

## 5. Verify the Publication

Once published, your package should be available at:
https://pypi.org/project/stableagents-ai/

Users can install it with:
```bash
pip install stableagents-ai
```

## Publishing New Versions

1. Update the version in `pyproject.toml`
2. Update the `__version__` in `stableagents/__init__.py`
3. Run `poetry publish --build` 