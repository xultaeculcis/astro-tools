### With `pip` for usage

Make sure you have Python=3.12+

```shell
pip install git+https://github.com/xultaeculcis/astro-tools.git
```

### With `uv` for development

1. Install `uv`

    ```shell
    !curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

2. Setup `astro-tools`

    ```shell
    git clone https://github.com/xultaeculcis/astro-tools.git
    cd astro-tools
    uv sync
    ```

3. Set env variables

    First, rename `.env-sample` to `.env`

    ```shell
    mv .env-sample .env
    ```

    And fill in your variables in `.env` file.

4. Run CLI

    ```shell
    astro-tools --help
    ```

Please, replace arguments with your values.
