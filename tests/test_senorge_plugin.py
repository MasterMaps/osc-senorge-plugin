import importlib.resources

import yaml

from osc_senorge_plugin.datasets.senorge import SeNorgePlugin

PLUGIN_PATH = "osc_senorge_plugin.datasets.senorge.SeNorgePlugin"


def _templates():
    res = importlib.resources.files("osc_senorge_plugin") / "datasets" / "senorge.yaml"
    return yaml.safe_load(res.read_text(encoding="utf-8"))


def test_templates_parse():
    templates = _templates()
    ids = {t["id"] for t in templates}
    assert ids == {
        "senorge_temperature_daily",
        "senorge_precipitation_daily",
        "senorge_temperature_daily_normal_1991_2020",
        "senorge_temperature_daily_anomaly_1991_2020",
    }
    # Source (ingestable) templates reference this plugin; derived ones are static.
    for t in templates:
        if t["sync"]["kind"] == "static":
            assert "ingestion" not in t
        else:
            assert t["ingestion"]["plugin"] == PLUGIN_PATH
            assert t["source_crs"] == "EPSG:32633"


def test_plugin_class_matches_template_crs():
    assert SeNorgePlugin.crs == 32633
    assert SeNorgePlugin(variable="tg") is not None
