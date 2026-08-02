# Open Climate Service — seNorge plugin

An installable [Open Climate Service](https://github.com/dhis2/open-climate-service) (OCS) plugin that
provides **seNorge 2018** daily climate data for Norway: mean temperature (`tg`) and precipitation (`rr`),
1 km × 1 km on the UTM33 grid (`EPSG:32633`), daily from 1957.

Data is downloaded from the Norwegian Meteorological Institute's THREDDS OPeNDAP service.

It is the reference implementation for OCS's installable-plugin mechanism
([dhis2/open-climate-service#118](https://github.com/dhis2/open-climate-service/issues/118)).

## Datasets

| id | variable | units |
| --- | --- | --- |
| `senorge_temperature_daily` | `tg` (daily mean temperature) | `degC` |
| `senorge_precipitation_daily` | `rr` (daily precipitation) | `mm/d` |

## Install

In an OCS instance, add the plugin and OCS auto-discovers it — no `plugins_dir` wiring:

```bash
uv add open-climate-service-senorge-plugin
```

Its datasets then appear in `/datasets` and can be ingested like any built-in dataset:

```bash
curl -X POST http://127.0.0.1:8000/ingestions \
  -H 'Content-Type: application/json' \
  -d '{"dataset_id": "senorge_temperature_daily", "temporal_extent": ["2024-01-01", "2024-01-31"]}'
```

Derived products (climatological normals, anomalies) are **instance-specific** — they are static
outputs of workflows run against these datasets and belong in the instance's own `plugins_dir`,
not in this download plugin.

## How it works

The package declares an `open_climate_service.plugins` entry point pointing at its top-level module.
OCS discovers all installed packages in that group and loads their `datasets/*.yaml` templates; the
ingestion plugin class (`open_climate_service_senorge_plugin.senorge.SeNorgePlugin`) is imported by
its dotted path at ingest time. `plugins_dir` continues to work and takes precedence on id conflicts.

## Layout

```
open_climate_service_senorge_plugin/
  senorge.py            # SeNorgePlugin (BaseDatasetPlugin)
  datasets/
    senorge.yaml        # dataset templates
```
