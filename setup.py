#!/usr/bin/env python3

# python setup.py sdist --format=zip,gztar

from setuptools import setup
import os
import sys
import platform
import imp
import argparse

with open('contrib/requirements/requirements.txt') as f:
    requirements = f.read().splitlines()

with open('contrib/requirements/requirements-hw.txt') as f:
    requirements_hw = f.read().splitlines()

version = imp.load_source('version', 'lib/version.py')

if sys.version_info[:3] < (3, 4, 0):
    sys.exit("Error: Electrum requires Python version >= 3.4.0...")

data_files = []

if platform.system() in ['Linux', 'FreeBSD', 'DragonFly']:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root=', dest='root_path', metavar='dir', default='/')
    opts, _ = parser.parse_known_args(sys.argv[1:])
    usr_share = os.path.join(sys.prefix, "share")
    icons_dirname = 'pixmaps'
    if not os.access(opts.root_path + usr_share, os.W_OK) and \
       not os.access(opts.root_path, os.W_OK):
        icons_dirname = 'icons'
        if 'XDG_DATA_HOME' in os.environ.keys():
            usr_share = os.environ['XDG_DATA_HOME']
        else:
            usr_share = os.path.expanduser('~/.local/share')
    data_files += [
        (os.path.join(usr_share, 'applications/'), ['electrum-mona.desktop']),
        (os.path.join(usr_share, icons_dirname), ['icons/electrum.png'])
    ]

extras_require = {
    'hardware': requirements_hw,
    'fast': ['pycryptodomex'],
    ':python_version < "3.5"': ['typing>=3.0.0'],
}
extras_require['full'] = extras_require['hardware'] + extras_require['fast']


setup(
    name="Electrum-MONA",
    version=version.ELECTRUM_VERSION,
    install_requires=requirements,
    extras_require=extras_require,
    packages=[
        'electrum_mona',
        'electrum_mona_gui',
        'electrum_mona_gui.qt',
        'electrum_mona_plugins',
        'electrum_mona_plugins.audio_modem',
        'electrum_mona_plugins.cosigner_pool',
        'electrum_mona_plugins.email_requests',
        'electrum_mona_plugins.greenaddress_instant',
        'electrum_mona_plugins.hw_wallet',
        'electrum_mona_plugins.keepkey',
        'electrum_mona_plugins.labels',
        'electrum_mona_plugins.ledger',
        'electrum_mona_plugins.revealer',
        'electrum_mona_plugins.trezor',
        'electrum_mona_plugins.digitalbitbox',
        'electrum_mona_plugins.virtualkeyboard',
    ],
    package_dir={
        'electrum_mona': 'lib',
        'electrum_mona_gui': 'gui',
        'electrum_mona_plugins': 'plugins',
    },
    package_data={
        '': ['*.txt', '*.json', '*.ttf', '*.otf'],
        'electrum_mona': [
            'locale/*/LC_MESSAGES/electrum.mo',
        ],
    },
    scripts=['electrum-mona'],
    data_files=data_files,
    description="Lightweight Monacoin Wallet",
    author="Thomas Voegtlin",
    author_email="thomasv@electrum.org",
    license="MIT Licence",
    url="https://github.com/wakiyamap/electrum-mona",
    long_description="""Lightweight Monacoin Wallet"""
)
