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

Putting the data onto ZFS with zstd compression will save ~1/3 disk space and speed up read operations. The DuckDB docs recommend XFS. XFS hwhich has not compression built in, but it can be layered over XFS.


# Usage

## Run an interactive ipython repl

```sh
steam-run uv run obis-repl
```

## Run the tests

```sh
steam-run uv run pytest
```

# Notes

## OBIS Datastructures

DuckDB has [2 types of datatypes](https://duckdb.org/docs/2.0/sql/data_types/overview), general-purpose data types (e.g. VARCHAR, INTEGER, BIGINT, GEOMETRY) and nested / composite types (ARRAY, LIST, MAP, STRUCT, TUPLE, and UNION). 

The OBIS dataset has only a view columns, but contains 3 STRUCTs that hold a lot of columns

General purpose:

 * _event_id: VARCHAR
 * _occurrence_id: VARCHAR
 * dataset_id: VARCHAR
 * node_ids: VARCHAR[]
 * missing: VARCHAR[]
 * invalid: VARCHAR[]
 * flags: VARCHAR[]
 * dropped: BOOLEAN
 * absence: BOOLEAN
 * tags: VARCHAR[]
 * geometry: GEOMETRY('OGC:CRS84')

Nested structs:

 * source: STRUCT
 * interpreted: STRUCT
 * extensions: STRUCT
 



## DUCKDB Performance

[Performance guide](https://duckdb.org/docs/2.0/guides/performance/overview)

### Engine / serialization

The clients embed the DuckDB C++ engine. The engine handles threading and async io internally. 

Beside the in engine time one of or the most costly thing will be converting to python objects.
There is a [page on conversion or results to python](https://duckdb.org/docs/2.0/clients/python/conversion). 

There are 2 types of queries / sources of results:

* the [relations api](https://duckdb.org/docs/2.0/clients/python/relational_api) (`.query()`, `.sql()`, ...)
* the python DB-API 2.0 API (`.execute()`)

Relations + Arrow tables/readers will be the most efficient way to work with data. The relations api internally works with the Arrow PyCapsule interface. From a relation we can get an arrow table (`.to_arrow_table()`) and reader (`.to_arrow_reader()`) without copying the data. Arrow tables can be serialized with `pyarrow.ipc`. Streaming a result in chunks should be:


``` python
class _ChunkSink:
    def __init__(self):
        self.chunks = []
        self.closed = False
    def write(self, data):
        self.chunks.append(bytes(data))
        return len(data)
    def flush(self):
        pass
    def close(self):
        self.closed = True
    def drain(self):
        out, self.chunks = b"".join(self.chunks), []
        return out

@app.route("/data-stream")
def get_data_stream():
    reader = my_query.to_arrow_reader()

    def generate():
        sink = _ChunkSink()
        with ipc.new_stream(pa.PythonFile(sink, mode="w"), reader.schema) as writer:
            for batch in reader:
                writer.write_batch(batch)
                yield sink.drain()
        yield sink.drain()  # end-of-stream marker

    return Response(generate(), mimetype="application/vnd.apache.arrow.stream")
```

In a Browser [Apache Arrow Javascript](https://arrow.apache.org/js/current/) can read the stream: 

``` typescript
import { tableFromIPC } from 'apache-arrow';
...
tableFromIPC(await fetch(url))

// which is

tableFromIPC<T extends TypeMap = any>(
    source: ArrowJSONLike | FromArg2,
): Table<T>


```

Both methods in the DB-API interface have to copy the data.

Converting to python types will have the usual high overhead. Creating Pandas or Polars data frames might be more efficient.

### Database characteristics

DuckDB has [support for basic indexes](https://duckdb.org/docs/2.0/guides/performance/indexing). 
There are Zone Map indexes and ART indexes. 

Zone map indexs are most effective on (semi) ordered columns. Ordering can also have a big impact on storage size. 

ART (Adaptive Radix Tree) indexes are created implicitly (PRIMARY KEY/FOREIGN KEY/UNIQUE) or with `CREATE INDEX`. If an ART index is loaded into memory this memory will not be freed, it needs `DETACH`/`ATTACH`.

There is `EXPLAIN ANALYZE`.
