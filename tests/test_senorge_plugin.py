import importlib.resources

import yaml

from open_climate_service_senorge_plugin.senorge import SeNorgePlugin


def _templates():
    res = importlib.resources.files("open_climate_service_senorge_plugin") / "datasets" / "senorge.yaml"
    return yaml.safe_load(res.read_text(encoding="utf-8"))


def test_templates_parse_and_reference_this_plugin():
    templates = _templates()
    ids = {t["id"] for t in templates}
    assert ids == {"senorge_temperature_daily", "senorge_precipitation_daily"}
    for t in templates:
        assert t["ingestion"]["plugin"] == "open_climate_service_senorge_plugin.senorge.SeNorgePlugin"
        assert t["source_crs"] == "EPSG:32633"


def test_plugin_class_matches_template_crs():
    assert SeNorgePlugin.crs == 32633
    plugin = SeNorgePlugin(variable="tg")
    assert plugin is not None
