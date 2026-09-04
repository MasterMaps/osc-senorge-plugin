# Open Climate Service — seNorge plugin

An installable [Open Climate Service](https://github.com/dhis2/open-climate-service) (OCS) plugin that
provides **seNorge 2018** daily climate data for Norway: mean temperature (`tg`) and precipitation (`rr`),
1 km × 1 km on the UTM33 grid (`EPSG:32633`), daily from 1957.

Data is downloaded from the Norwegian Meteorological Institute's THREDDS OPeNDAP service.

It is the reference implementation for OCS's installable-plugin mechanism
([dhis2/open-climate-service#118](https://github.com/dhis2/open-climate-service/issues/118)).

## Datasets

| id | kind | notes |
| --- | --- | --- |
| `senorge_temperature_daily` | source (`tg`, `degC`) | downloaded by `SeNorgePlugin` |
| `senorge_precipitation_daily` | source (`rr`, `mm/d`) | downloaded by `SeNorgePlugin` |
| `senorge_temperature_daily_normal_1991_2020` | derived (static) | day-of-year normal via the `climate_normal` workflow |
| `senorge_temperature_daily_anomaly_1991_2020` | derived (static) | daily anomaly via the `climate_anomaly` workflow |

## Install

In an OCS instance, add the plugin and OCS auto-discovers it — no `plugins_dir` wiring. Not published
to PyPI, so install from git:

```bash
uv add "osc-senorge-plugin @ git+https://github.com/MasterMaps/osc-senorge-plugin.git"
```

Pin a branch or tag through the instance's own `[tool.uv.sources]` if you need one:

```toml
[tool.uv.sources]
osc-senorge-plugin = { git = "https://github.com/MasterMaps/osc-senorge-plugin.git", branch = "main" }
```

Its datasets then appear in `/datasets` and can be ingested like any built-in dataset:

```bash
curl -X POST http://127.0.0.1:8000/ingestions \
  -H 'Content-Type: application/json' \
  -d '{"dataset_id": "senorge_temperature_daily", "temporal_extent": ["2024-01-01", "2024-01-31"]}'
```

The derived normal/anomaly datasets are **static** templates: their data is written by the OCS
built-in `climate_normal` / `climate_anomaly` workflows run against the source datasets. They ship
here so the whole seNorge family installs as one plugin.

## How it works

The package declares an `open_climate_service.plugins` entry point pointing at its top-level package.
OCS discovers all installed packages in that group and loads their `datasets/*.yaml` templates (and,
if present, their `processes/` and `workflows/`); the ingestion plugin class
(`osc_senorge_plugin.datasets.senorge.SeNorgePlugin`) is imported by its dotted path at ingest time.
`plugins_dir` continues to work and takes precedence on id conflicts.

## Layout

```
osc_senorge_plugin/
  datasets/
    senorge.py          # SeNorgePlugin (BaseDatasetPlugin)
    senorge.yaml        # dataset templates
  # processes/          # optional: @process-decorated callables
  # workflows/          # optional: openEO UDP JSON graphs
```
