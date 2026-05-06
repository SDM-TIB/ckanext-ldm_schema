import json

import six
from ckantoolkit import (
    missing,
    StopOnError,
    _
)

from ckanext.scheming.validation import scheming_validator


@scheming_validator
def scheming_auto_update_source(field, schema):
    """
    not_empty if field auto_update is different from 'No' else ignore_missing
    """
    def validator(key, data, errors, context):
        if (key[0], key[1], 'auto_update') in data:
            auto_update_field = str(data[(key[0], key[1], 'auto_update')])
        else:
            auto_update_field = 'No'

        if auto_update_field != 'No' and data[key] == '':
            errors[key].append(_('Automatic update is set then Update URL is required'))

    return validator


@scheming_validator
def scheming_multiple_text(field, schema):
    """
    Accept repeating text input in the following forms and convert to a json list
    for storage. Also act like scheming_required to check for at least one non-empty
    string when required is true:

    1. a list of strings, eg.

       ["Person One", "Person Two"]

    2. a single string value to allow single text fields to be
       migrated to repeating text

       "Person One"
    """
    def _scheming_multiple_text(key, data, errors, context):
        # just in case there was an error before our validator,
        # bail out here because our errors won't be useful
        if errors[key]:
            return

        value = data[key]
        # 1. list of strings or 2. single string
        if value is not missing:
            if isinstance(value, six.string_types):
                value = [value]
            if not isinstance(value, list):
                errors[key].append(_('expecting list of strings'))
                raise StopOnError

            out = []
            for element in value:
                if not element:
                    continue

                if not isinstance(element, six.string_types):
                    errors[key].append(_('invalid type for repeating text: %r')
                                       % element)
                    continue
                if isinstance(element, six.binary_type):
                    try:
                        element = element.decode('utf-8')
                    except UnicodeDecodeError:
                        errors[key]. append(_('invalid encoding for "%s" value')
                                            % element)
                        continue

                out.append(element)

            if errors[key]:
                raise StopOnError

            data[key] = json.dumps(out)

        if (data[key] is missing or data[key] == '[]') and field.get('required'):
            errors[key].append(_('Missing value'))
            raise StopOnError
        if data[key] is missing or data[key] == '[]':
            data[key] = ''  # fix insert of missing into DB

    return _scheming_multiple_text
