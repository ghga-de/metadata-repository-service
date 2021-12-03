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
Convenience methods for retrieving Publication records
"""

from typing import List

from metadata_repository_service.config import get_config
from metadata_repository_service.core.utils import embed_references
from metadata_repository_service.dao.db import get_db_client
from metadata_repository_service.models import Publication

COLLECTION_NAME = "Publication"

config = get_config()


async def retrieve_publications() -> List[str]:
    """
    Retrieve a list of Publication object IDs from metadata store.

    Returns:
        A list of Publication object IDs.

    """
    client = await get_db_client()
    collection = client[config.db_name][COLLECTION_NAME]
    publications = await collection.find().to_list(None)  # type: ignore
    client.close()
    return [x["id"] for x in publications]


async def get_publication(publication_id: str, embedded: bool = False) -> Publication:
    """
    Given a Datset ID, get the Publication object from metadata store.

    Args:
        publication_id: The Publication ID
        embedded: Whether or not to embed references. ``False``, by default.

    Returns:
        The Publication object

    """
    client = await get_db_client()
    collection = client[config.db_name][COLLECTION_NAME]
    publication = await collection.find_one({"id": publication_id})  # type: ignore
    if publication and embedded:
        publication = await embed_references(publication)
    client.close()
    return publication
