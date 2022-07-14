# Copyright 2021 - 2022 Universität Tübingen, DKFZ and EMBL
# for the German Human Genome-Phenome Archive (GHGA)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Config Parameter Modeling and Parsing"""

from ghga_service_chassis_lib.api import ApiConfigBase
from ghga_service_chassis_lib.config import config_from_yaml


@config_from_yaml(prefix="metadata_repository_service")
class Config(ApiConfigBase):
    """Config parameters and their defaults."""

    # config parameter needed for the api server
    # are inherited from ApiConfigBase;
    # config parameter needed for the api server
    # are inherited from PubSubConfigBase;
    db_url: str = "mongodb://localhost:27017"
    db_name: str = "metadata-store"
    schema_url: str = "https://raw.githubusercontent.com/ghga-de/ghga-metadata-schema/0.7.0/src/schema/ghga.yaml"
    creation_schema_url: str = "https://raw.githubusercontent.com/ghga-de/ghga-metadata-schema/0.7.0/artifacts/derived_schema/creation/ghga_creation.yaml"


CONFIG = Config()
