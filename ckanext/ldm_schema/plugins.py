import ckan.model as model
import ckan.plugins as p
import ckan.plugins.toolkit as toolkit

from ckanext.ldm_schema import helpers
from ckanext.ldm_schema import tib_services_cli
from ckanext.ldm_schema import validation
from ckanext.ldm_schema.tib_resource_autoupdate import *
from ckanext.ldm_schema.tib_services import update_service_dataset_relationship, add_service_data_to_dataset_show

STOP_UPDATE = True

log = logging.getLogger(__name__)


def get_paper_link_by_doi(doi):
    if "https://doi.org/" in doi:
        doi = doi.replace("https://doi.org/", "")
    search_url = f"https://orkg.org/api/papers?doi={doi}"

    response = requests.get(search_url)

    if response.status_code == 200:
        data = response.json()
        if data["content"] != []:
            paper_id = data["content"][0]['id']
            paper_url = f"http://orkg.org/orkg/resource/{paper_id}"
            if paper_url == "http://orkg.org/orkg/resource/R1000":
                return ""
            else:
                return paper_url
        else:
            log.info("Paper not found in ORKG.")
            return None
    else:
        log.info(f"Error: {response.status_code}")
        return None


class LDMSchemaPlugin(p.SingletonPlugin):
    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IValidators)
    p.implements(p.ITemplateHelpers)
    p.implements(p.IPackageController, inherit=True)
    p.implements(p.IClick)
    p.implements(p.IFacets, inherit=True)

    # Add resources updates
    TIB_RU_tool = TIB_resource_update_tool()
    TIB_RU_tool.create_cronjobs()

    def connecting_LDM_to_ORKG(self,context,pkg_dict):
        global STOP_UPDATE
        STOP_UPDATE = False
        #log.info(str(STOP_UPDATE))
        package_id = pkg_dict.get('id')
        if "defined_in" in pkg_dict:
            doi = pkg_dict['defined_in']
            if doi != "" and doi is not None:
                orkg = get_paper_link_by_doi(doi)
            else:
                orkg = ""
            pkg = model.Package.get(package_id)
            if orkg == "" or orkg is None:
                new_value = ""
            else:
                #self._save_to_package_extra(package_id, 'Link to ORKG', orkg)
                new_value = orkg

            pkg_dict = toolkit.get_action('package_show')(context, {'id': package_id})

            # Update the specific field value
            if pkg_dict['link_orkg'] != new_value:
                pkg_dict['link_orkg'] = new_value
                #log.info(pkg_dict)
                #log.info(new_value)
                # Call package_update to update the package
                updated_package = toolkit.get_action('package_update')(context, pkg_dict)

    def _save_to_package_extra(self, package_id, key, value):
        # Create or update a custom field in the package_extra table
        package_extra = model.Session.query(model.PackageExtra).filter_by(
            package_id=package_id, key=key).first()
        if package_extra:
            package_extra.value = value
        else:
            package_extra = model.PackageExtra(
                package_id=package_id,
                key=key,
                value=value
            )
            model.Session.add(package_extra)

        model.Session.commit()

    def delete_custom_value(self, context, data_dict):
        package_id = data_dict.get('package_id')
        key = 'Link to ORKG'

        if not package_id or not key:
            raise toolkit.ValidationError('package_id and key are required')

        package_extra = model.Session.query(model.PackageExtra).filter_by(
            package_id=package_id, key=key).first()

        if package_extra:
            model.Session.delete(package_extra)
            model.Session.commit()
            return {'success': True, 'message': 'Custom value removed successfully.'}
        else:
            return {'success': False, 'message': 'Custom value not found.'}

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_resource('assets', 'ckanext-ldm_schema')

    # IValidators
    def get_validators(self):
        return {
            'scheming_auto_update_source': validation.scheming_auto_update_source,
            'scheming_multiple_text': validation.scheming_multiple_text,
        }

    # ITemplateHelpers
    def get_helpers(self):
        return {
            'scheming_digital_objects_filter_title': helpers.scheming_digital_objects_filter_title,
            'scheming_get_local_datasets_for_services': helpers.scheming_get_local_datasets_for_services,
            'scheming_get_local_services_for_datasets': helpers.scheming_get_local_services_for_datasets,
            'scheming_get_services_for_dataset_display': helpers.scheming_get_services_for_dataset_display,
            'scheming_get_datasets_for_service_display': helpers.scheming_get_datasets_for_service_display,
            'is_doi_plugin_enabled': helpers.is_doi_plugin_enabled,
            'scheming_get_section': helpers.scheming_get_section,
        }

    # IClick
    def get_commands(self):
        return tib_services_cli.get_commands()

    # IFacets
    def dataset_facets(self, facets_dict, package_type):
        """Add new search facet (filter) for datasets.
        This must be a field in the dataset (or organization or
        group if you're modifying those search facets, just change the function).
        """
        # This adds the filter at top.
        facets_dict.update({'type': p.toolkit._('Object Type')})
        facets_dict.move_to_end('type', last=False)

        # Return the updated facet dict.
        return facets_dict

    # IPackageController (used for the datasets - services relationship)
    def after_update(self, context, pkg_dict):
        """Dataset has been created/updated. Check type of dataset and manage the relation between datasets-services"""
        log.info("Adding service-datasets relationships to Database\n")

        global STOP_UPDATE
        if STOP_UPDATE:
            update_service_dataset_relationship(pkg_dict)
            self.connecting_LDM_to_ORKG(context,pkg_dict)
        else:
            STOP_UPDATE = True

    def after_create(self, context, pkg_dict):
        """A new dataset/service has been created, so we need to add the dataset-service relationship to de DB.
        NB: This is called after creation of a dataset, before resources have been
        added, so state = draft.
        """
        log.info("Adding service-datasets relationships to Database\n")

        update_service_dataset_relationship(pkg_dict)
        self.connecting_LDM_to_ORKG(context,pkg_dict)

    # IPackageController
    def after_show(self, context, pkg_dict):
        """Add the Services details to the pkg_dict so it can be displayed."""
        # Patch avoiding error with operations without user logged
        # as update resources in resource autoupdate plugin
        if 'user' in context and context['user']:
            pkg_dict = add_service_data_to_dataset_show(pkg_dict)
