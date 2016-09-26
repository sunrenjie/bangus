#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


import os
from six.moves import xrange

from os import walk, path

MODULE_EXT = '.module.js'
MOCK_EXT = '.mock.js'
SPEC_EXT = '.spec.js'


def collect_dirs(prefix):
    return [d for d in os.listdir(prefix) if os.path.isdir(os.path.join(prefix, d))]


def collect_bower_static_libs(bower_prefix, static_prefix):
    dirs = []
    for d in collect_dirs(bower_prefix):
        dirs.append(('%s/lib/%s' % (static_prefix, d),
             os.path.abspath(os.path.join(bower_prefix, d))))
    return dirs


def populate_config_with_static_files(config, paths):
    cats = ['js_sources', 'js_mocks', 'js_specs', 'html_templates']
    for c in cats:
        if c not in config:
            config[c] = []
    for p in paths:
        r = list(collect_static_files(p))
        for i in xrange(0, len(cats)):
            config[cats[i]].extend(r[i])


def collect_static_files(prefix):
    js_files = collect_files(prefix, ext='.js', relative=True)
    srcs, mocks, specs = sort_js_files(js_files)
    html_files = collect_files(prefix, ext='.html', relative=True)
    return srcs, mocks, specs, html_files


def collect_files(prefix, ext='', relative=False):
    if not prefix.endswith('/'):
        prefix += '/'
    file_list = []

    for root, dirs, files in walk(prefix):
        if relative:
            root = root.replace(prefix, '', 1)
        file_list.extend([path.join(root, f)
                          for f in files if f.endswith(ext)])
    return sorted(file_list)


def sort_js_files(js_files):
    """Sorts JavaScript files in `js_files` into source files, mock files
    and spec files based on file extension.

    Output:

    * sources: source files for production.  The order of source files
      is significant and should be listed in the below order:

      - First, all the that defines the other application's angular module.
        Those files have extension of `.module.js`.  The order among them is
        not significant.

      - Followed by all other source code files.  The order among them
        is not significant.

    * mocks: mock files provide mock data/services for tests.  They have
      extension of `.mock.js`. The order among them is not significant.

    * specs: spec files for testing.  They have extension of `.spec.js`.
      The order among them is not significant.

    """
    modules = [f for f in js_files if f.endswith(MODULE_EXT)]
    mocks = [f for f in js_files if f.endswith(MOCK_EXT)]
    specs = [f for f in js_files if f.endswith(SPEC_EXT)]

    other_sources = [f for f in js_files if
                     not f.endswith(MODULE_EXT)
                     and not f.endswith(MOCK_EXT)
                     and not f.endswith(SPEC_EXT)]

    sources = modules + other_sources
    return sources, mocks, specs
