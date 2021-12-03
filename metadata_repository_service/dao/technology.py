# Copyright 2021 Universität Tübingen, DKFZ and EMBL
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
"""
Convenience methods for retrieving Technology records
"""

from typing import List

from metadata_repository_service.config import Config, get_config
from metadata_repository_service.core.utils import embed_references
from metadata_repository_service.dao.db import get_db_client
from metadata_repository_service.models import Technology

COLLECTION_NAME = "Technology"


async def retrieve_technologies(config: Config = get_config()) -> List[str]:
    """
    Retrieve a list of Technology object IDs from metadata store.

    Args:
        config: Rumtime configuration

    Returns:
        A list of Technology object IDs.

    """
    client = await get_db_client()
    collection = client[config.db_name][COLLECTION_NAME]
    technologies = await collection.find().to_list(None)  # type: ignore
    client.close()
    return [x["id"] for x in technologies]


async def get_technology(
    technology_id: str, embedded: bool = False, config: Config = get_config()
) -> Technology:
    """
    Given an Technology ID, get the Technology object from metadata store.

    Args:
        technology_id: The Technology ID
        embedded: Whether or not to embed references. ``False``, by default.
        config: Rumtime configuration

    Returns:
        The Technology object

    """
    client = await get_db_client()
    collection = client[config.db_name][COLLECTION_NAME]
    technology = await collection.find_one({"id": technology_id})  # type: ignore
    if technology and embedded:
        technology = await embed_references(technology)
    client.close()
    return technology
