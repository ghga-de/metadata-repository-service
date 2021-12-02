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
Convenience methods for retrieving Individual records
"""

from typing import List

from fastapi.exceptions import HTTPException

from metadata_repository_service.config import get_config
from metadata_repository_service.core.utils import embed_references
from metadata_repository_service.dao.db import get_db_client
from metadata_repository_service.models import Individual

COLLECTION_NAME = "Individual"

config = get_config()


async def retrieve_individuals() -> List[str]:
    """
    Retrieve a list of Individual object IDs from metadata store.

    Returns:
        A list of Individual object IDs.

    """
    client = await get_db_client()
    collection = client[config.db_name][COLLECTION_NAME]
    individuals = await collection.find().to_list(None)  # type: ignore
    client.close()
    return [x["id"] for x in individuals]


async def get_individual(individual_id: str, embedded: bool = False) -> Individual:
    """
    Given a Datset ID, get the Individual object from metadata store.

    Args:
        individual_id: The Individual ID
        embedded: Whether or not to embed references. ``False``, by default.

    Returns:
        The Individual object

    """
    client = await get_db_client()
    collection = client[config.db_name][COLLECTION_NAME]
    individual = await collection.find_one({"id": individual_id})  # type: ignore
    if not individual:
        raise HTTPException(
            status_code=404,
            detail=f"{Individual.__name__} with id '{individual_id}' not found",
        )
    if embedded:
        individual = await embed_references(individual)
    client.close()
    return individual
