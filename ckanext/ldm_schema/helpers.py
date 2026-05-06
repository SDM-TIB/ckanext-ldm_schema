from ckan.plugins import toolkit
from ckanext.ldm_schema.tib_services import get_local_datasets_for_services, get_local_services_for_datasets, \
    get_services_for_dataset_display, get_datasets_for_service_display
from ckantoolkit import config


def scheming_digital_objects_filter_title():
    data = {'dataset': 'Local Dataset',
            'vdataset': 'Imported Dataset',
            'service': 'Service',
            'github': 'GitHub'
            }
    return data


def scheming_get_local_datasets_for_services(service_id):
    return get_local_datasets_for_services(toolkit.g.user, service_id)


def scheming_get_local_services_for_datasets(dataset_id):
    return get_local_services_for_datasets(toolkit.g.user, dataset_id)


def scheming_get_services_for_dataset_display(ds_id):
    return get_services_for_dataset_display(ds_id)


def scheming_get_datasets_for_service_display(service_id):
    return get_datasets_for_service_display(service_id)


def is_doi_plugin_enabled():
    doi_installed = 'doi' in config.get('ckan.plugins', "")
    return doi_installed
