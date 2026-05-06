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
