import re

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources
import gettext


def format_chemical_formula(formula):
    items = re.findall(r"[A-Za-z() -*%.+*/]+|[0-9]+", formula, re.I)
    if items:
        for idx in range(len(items)):
            if items[idx].isnumeric():
                items[idx] = "$_{" + items[idx] + "}$"
        return ''.join(items)
    return formula


def get_translator(lang_cfg):
    if lang_cfg is not None and lang_cfg['lang'] is not None:
        lang = lang_cfg['lang']
        if 'domain' in lang_cfg.keys():
            domain = lang_cfg['domain']
        else:
            domain = 'gg'
        if 'locales' in lang_cfg.keys():
            locales = lang_cfg['locales']
        else:
            locales = 'locales'

        locales_path = pkg_resources.files(locales).joinpath("")
        el = gettext.translation(domain, localedir=str(locales_path), languages=[lang, ])
        el.install()
        return el.gettext

    return gettext.gettext
