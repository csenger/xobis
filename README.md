# xobis - Experiments with the OBIS dataset and duckdb

https://github.com/iobis/obis-open-data

# Prerequisits

## uv / Python / steam-run

You need to have `uv` and a recent Python version installed, tested with 3.14.10. `steam-run` is only required on NixOS to have required shared libraries available.

## OBIS data

Download the dataset and put the occurence directory with the parquet files into `./obis-open-data/occurrence`.
https://github.com/iobis/obis-open-data#downloading-the-dataset

```sh
nix-shell -p awscli2
aws s3 sync --no-sign-request s3://obis-open-data/occurrence/ ./obis-open-data/occurrence/
```

Putting the data onto ZFS with zstd compression will save ~1/3 disk space and speed up read operations. 


# Usage

## Run an interactive ipython repl

```sh
steam-run uv run obis-repl
```

## Run the tests

```sh
steam-run uv run pytest
```

