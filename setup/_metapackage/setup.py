import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-akretion-vertical-bike",
    description="Meta package for akretion-vertical-bike Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-bicycode',
        'odoo14-addon-shopinvader_bicycode',
        'odoo14-addon-shopinvader_delivery_detail',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
