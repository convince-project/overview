project = 'CONVINCE Toolbox Overview'
copyright = '2026'
author = 'CONVINCE Consortium'

release = '1.0'
version = '1.0.0'

extensions = [
    'sphinx.ext.intersphinx',
    'sphinx_mdinclude',
]
templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'
html_logo = 'convince_logo_horizontal_200p.png'
html_static_path = ['_static']
html_style = 'css/custom.css'

# this allows to reference the images relative to the tutorials folder in md and also sphinx to find them from html
html_extra_path = ['../../tutorials/', '../../tutorials/refine_plan_demo/']