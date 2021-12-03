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
Convenience methods for retrieving DataAccessPolicy records
"""

from typing import List

from metadata_repository_service.config import get_config
from metadata_repository_service.core.utils import embed_references
from metadata_repository_service.dao.db import get_db_client
from metadata_repository_service.models import DataAccessPolicy

COLLECTION_NAME = "DataAccessPolicy"

config = get_config()


async def retrieve_data_access_policies() -> List[str]:
    """
    Retrieve a list of DataAccessPolicy object IDs from metadata store.

    Returns:
        A list of DataAccessPolicy object IDs.

    """
    client = await get_db_client()
    collection = client[config.db_name][COLLECTION_NAME]
    data_access_policies = await collection.find().to_list(None)  # type: ignore
    client.close()
    return [x["id"] for x in data_access_policies]


async def get_data_access_policy(
    data_access_policy_id: str, embedded: bool = False
) -> DataAccessPolicy:
    """
    Given a Datset ID, get the DataAccessPolicy object from metadata store.

    Args:
        data_access_policy_id: The DataAccessPolicy ID
        embedded: Whether or not to embed references. ``False``, by default.

    Returns:
        The DataAccessPolicy object

    """
    client = await get_db_client()
    collection = client[config.db_name][COLLECTION_NAME]
    data_access_policy = await collection.find_one({"id": data_access_policy_id})  # type: ignore
    if data_access_policy and embedded:
        data_access_policy = await embed_references(data_access_policy)
    client.close()
    return data_access_policy
