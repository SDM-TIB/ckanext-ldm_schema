[![Latest Release](http://img.shields.io/github/release/SDM-TIB/ckanext-ldm_schema.svg?logo=github)](https://github.com/SDM-TIB/ckanext-ldm_schema/releases)
[![License: GPL v3](https://img.shields.io/github/license/SDM-TIB/ckanext-ldm_schema?color=blue)](LICENSE.md)

[![CKAN](https://img.shields.io/badge/ckan-2.9-orange.svg?style=flat)](https://github.com/ckan/ckan)

# ckanext-ldm_schema

This CKAN extension provides the schema used by the [Leibniz Data Manager](https://github.com/SDM-TIB/LDM_Docker) (LDM)
and is built on [`ckanext-scheming`](https://github.com/ckan/ckanext-scheming).

## Requirements

| CKAN version    | Compatibility |
|-----------------|---------------|
| 2.8 and earlier | No |
| 2.9             | Yes |
| 2.10 and later  | Unknown |

Designed to work with CKAN 2.9.

This extension also requires `ckanext-scheming` to be installed. 

## Additional Features

`ckanext-ldm_schema` extends `ckanext-scheming` with collapsible sections.
Sections are defined at their own top-level entry in the yaml files, e.g.:

```yaml
sections:
  - section_id: geospatial
    title: Geospatial Information
    subtitle: Address or extend covered by the data
  - section_id: temporal
    title: Temporal Information
    subtitle: Reference date or timeseries covered by the data
```

The `dataset` and `resource` fields can then use these sections by adding `section_id`.
Note that, there will be one collapsible section for all subsequent fields with the same section mentioned.
The example below will create two collapsible sections for the sections defined above.

```yaml
  - field_name: address
    label: Address
    section_id: geospatial
  - field_name: latitude
    label: Latitude
    section_id: geospatial
  - field_name: Longitude
    label: Longitude
    section_id: geospatial

  - field_name: temporal_timeseries_start
    label: Start
    form_snippet: scheming/form_snippets/datetime_local.html
    display_snippet: scheming/display_snippets/datetime_local.html
    validators: ignore_missing normalize_datetime
    section_id: temporal
  - field_name: temporal_timeseries_end
    label: End
    form_snippet: scheming/form_snippets/datetime_local.html
    display_snippet: scheming/display_snippets/datetime_local.html
    validators: ignore_missing normalize_datetime
    section_id: temporal
```

## Installation

As usual for CKAN extensions, you can install `ckanext-ldm_schema` as follows:

```bash
pip install -e "git+https://github.com/SDM-TIB/ckanext-ldm_schema#egg=ckanext-ldm_schema"
```

## Configuration

Set the schemas you want to use with configuration options:

```ini
ckan.plugins = ldm_schema scheming_tibupdateresources scheming_datasets 

scheming.dataset_schemas = ckanext.ldm_schema:schemas/ckan_dataset.yaml
                           ckanext.ldm_schema:schemas/ckan_vdataset.yaml
                           ckanext.ldm_schema:schemas/service.yaml

scheming.presets = ckanext.scheming:presets.json
                   ckanext.ldm_schema:presets/presets.json

# Configuration options for the resource updates
scheming_tibupdateresources_enabled = true
scheming_tibupdateresources_crontab_user = root
ckan.extra_resource_fields = auto_update
```

## Changelog

If you are interested in what has changed, check out the [changelog](CHANGELOG.md).

## License

`ckanext-ldm_schema` is licensed under GPL-3.0, see the [license file](LICENSE).
