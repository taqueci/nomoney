# Copyright (C) Takeshi Nakamura. All rights reserved.

"""TinyMCE configuration."""

TINYMCE_DEFAULT_CONFIG = {
    'height': 360,
    'body_class': 'doc-content',
    'content_style': '.mce-content-body { margin: 8px; }',
    'verify_html': False,
    'menubar': False,
    'plugins': 'advlist anchor code code codesample fullscreen help hr image'
    ' link lists media paste preview searchreplace table toc visualblocks'
    ' wordcount',
    'toolbar': 'fullscreen preview visualblocks'
    '| undo redo | searchreplace'
    '| styleselect| bold italic underline strikethrough'
    '| alignleft aligncenter alignright'
    '| outdent indent | hr | numlist bullist | table tablerowheader'
    '| forecolor backcolor removeformat | image link anchor codesample toc'
    '| code | help',
    'toolbar_mode': 'wrap',
    'relative_urls': False,
    'remove_script_host': True,
    'table_header_type': 'sectionCells',
    'table_default_attributes': {'class': 'table table-light'},
    'table_default_styles': {},
    'visual_table_class': 'table',
    'file_picker_types': 'file image',
    'style_formats': [{
        'title': 'Alerts', 'items': [{
            'title': 'Alert (Primary)', 'wrapper': True,
            'block': 'div', 'classes': 'alert alert-primary',
        }, {
            'title': 'Alert (Secondary)', 'wrapper': True,
            'block': 'div', 'classes': 'alert alert-secondary',
        }, {
            'title': 'Alert (Suucess)', 'wrapper': True,
            'block': 'div', 'classes': 'alert alert-success',
        }, {
            'title': 'Alert (Danger)', 'wrapper': True,
            'block': 'div', 'classes': 'alert alert-danger',
        }, {
            'title': 'Alert (Warning)', 'wrapper': True,
            'block': 'div', 'classes': 'alert alert-warning',
        }, {
            'title': 'Alert (Info)', 'wrapper': True,
            'block': 'div', 'classes': 'alert alert-info',
        }, {
            'title': 'Alert (Light)', 'wrapper': True,
            'block': 'div', 'classes': 'alert alert-light',
        }, {
            'title': 'Alert (Dark)', 'wrapper': True,
            'block': 'div', 'classes': 'alert alert-dark',
        }]
    }, {
        'title': 'Badges', 'items': [{
            'title': 'Badge (Primary)',
            'inline': 'span', 'classes': 'badge bg-primary',
        }, {
            'title': 'Badge (Secondary)',
            'inline': 'span', 'classes': 'badge bg-secondary',
        }, {
            'title': 'Badge (Success)',
            'inline': 'span', 'classes': 'badge bg-success',
        }, {
            'title': 'Badge (Danger)',
            'inline': 'span', 'classes': 'badge bg-danger',
        }, {
            'title': 'Badge (Warning)',
            'inline': 'span', 'classes': 'badge bg-warning',
        }, {
            'title': 'Badge (Info)',
            'inline': 'span', 'classes': 'badge bg-info',
        }, {
            'title': 'Badge (Light)',
            'inline': 'span', 'classes': 'badge bg-light',
        }, {
            'title': 'Badge (Dark)',
            'inline': 'span', 'classes': 'badge bg-dark',
        }]
    }, {
        'title': 'Colors', 'items': [{
            'title': 'Primary', 'inline': 'span', 'classes': 'text-primary',
        }, {
            'title': 'Secondary', 'inline': 'span', 'classes': 'text-secondary',
        }, {
            'title': 'Success', 'inline': 'span', 'classes': 'text-success',
        }, {
            'title': 'Danger', 'inline': 'span', 'classes': 'text-danger',
        }, {
            'title': 'Warning', 'inline': 'span', 'classes': 'text-warning',
        }, {
            'title': 'Info', 'inline': 'span', 'classes': 'text-info',
        }, {
            'title': 'Light', 'inline': 'span', 'classes': 'text-light',
        }, {
            'title': 'Muted', 'inline': 'span', 'classes': 'text-muted',
        }]
    }, {
        'title': 'Typography', 'items': [{
            'title': 'Lead', 'block': 'p', 'classes': 'lead',
        }, {
            'title': 'Blockquote',
            'block': 'blockquote', 'classes': 'blockquote',
        }]
    }],
    'codesample_languages': [
        {'text': 'Text', 'value': 'text'},
        {'text': 'Shell', 'value': 'shell'},
        {'text': 'JSON', 'value': 'json'},
        {'text': 'YAML', 'value': 'yaml'},
        {'text': 'HTML/XML', 'value': 'markup'},
        {'text': 'JavaScript', 'value': 'javascript'},
        {'text': 'CSS', 'value': 'css'},
        {'text': 'Python', 'value': 'python'},
        {'text': 'Java', 'value': 'java'},
        {'text': 'C', 'value': 'c'},
        {'text': 'C++', 'value': 'cpp'},
        {'text': 'SQL', 'value': 'sql'},
        {'text': 'Diff', 'value': 'diff'},
    ],
    'toc_header': 'h5',
    'toc_class': 'doc-toc bg-light rounded-2 p-3',
    'style_formats_merge': True,
}
