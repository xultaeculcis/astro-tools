`astro-tools` provides set of Astrophotography tools for managing data assets and running automated image processing.

Below, you'll find basic usage scenarios for the `astro-tools` CLI.

## Checking for ZIP corruption

### Fast Check

Fast check by trying to only list zip contents:

```shell
astro-tools zip check \
    --directory=/home/xultaeculcis/Downloads \
    --log_file=telescope-live.log \
    --workers=10 \
    --fast
```

Please, replace arguments with your values.

### Full Check

Full check by running zip test:

```shell
astro-tools zip check \
    --directory=/home/xultaeculcis/Downloads \
    --log_file=telescope-live.log \
    --workers=10 \
    --full
```

Please, replace arguments with your values.

## Renaming Telescope.Live ZIPs

After downloading you Telescope.Live data you can run:

```shell
astro-tools zip rename --data_dir=/home/xultaeculcis/Downloads
```

To rename the ZIP files to follow this pattern: `<TARGET_NAME>_<TELESCOPE>_<FILTERS>_<FRAMES>[-<OBSERVATION_NUMBER>].zip`.

## Creating directories

Assuming you have created a `names.txt` file with list of directory names to create with following contents:

```text
arp-319-stephans-quintet-in-pegasus
ic-5076-reflection-nebula-in-cygnus
ngc-247-needles-eye-galaxy-in-cetus
ngc-488-face-on-spiral-galaxy-in-pisces
ngc-1313-topsy-turvy-galaxy
ngc-1531-dwarf-galaxy-in-eridanus
```

Then you can run:

```shell
astro-tools dir create \
    --names_fp ./data/names.txt \
    --target_dir=/home/xultaeculcis/Downloads
```

The tool will create directories for you:

```text
/home/xultaeculcis/Downloads/
├── arp-319-stephans-quintet-in-pegasus
├── ic-5076-reflection-nebula-in-cygnus
├── ngc-1313-topsy-turvy-galaxy
├── ngc-1531-dwarf-galaxy-in-eridanus
├── ngc-247-needles-eye-galaxy-in-cetus
└── ngc-488-face-on-spiral-galaxy-in-pisces
```

Please, replace arguments with your values.

## Uploading data to blob storage

### From local

Run:

```shell
astro-tools blob upload \
    --source_dir=/home/xultaeculcis/Downloads \
    --log_dir=./blob-upload-logs \
    --container=datasets \
    --prefix=telescope-live/raw-zips \
    --workers=10
```

Please, replace arguments with your values.

### From Google Drive using Colab

Let's assume you have a shortcut to shared GDrive folder called `Astrophoto_Release` inside
your GDrive folder called `Shared`.

1. Mount the drive

    ```python
    from google.colab import drive
    drive.mount('/content/drive')
    ```

2. Verify drive contents

    ```shell
    !ls -la "/content/drive/MyDrive/Shared/Astrophoto_Release/"
    ```

3. Setup `astro-tools`

    ```shell
    !pip install git+https://github.com/xultaeculcis/astro-tools.git
    ```

4. Set env variables

    ```shell
    !export BLOB__ACCOUNT_NAME=...
    !export BLOB__ACCOUNT_KEY=...
    ```

    And fill in your variables in `.env` file.

5. Run CLI

    ```shell
    !astro-tools blob upload \
      --source_dir=/content/drive/MyDrive/Shared/Astrophoto_Release/ \
      --log_dir=./blob-upload-logs \
      --container=datasets \
      --prefix=whwang/gdrive-export
    ```

Please, replace arguments with your values.
