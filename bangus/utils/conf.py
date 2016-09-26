# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import copy
from django.utils.functional import empty, LazyObject, SimpleLazyObject


class LazyConf(LazyObject):
    def _setup(self, name=None):
        from django.conf import settings
        config = settings.CONFIG

        self._wrapped = config

    def __getitem__(self, name, fallback=None):
        if self._wrapped is empty:
            self._setup(name)
        return self._wrapped.get(name, fallback)


CONFIG = LazyConf()
