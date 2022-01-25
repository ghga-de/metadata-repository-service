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
"""
Convenience methods for retrieving DataAccessCommittee records
"""

from typing import List

from metadata_repository_service.config import CONFIG, Config
from metadata_repository_service.core.utils import embed_references
from metadata_repository_service.dao.db import get_db_client
from metadata_repository_service.models import DataAccessCommittee

COLLECTION_NAME = "DataAccessCommittee"


async def retrieve_data_access_committees(config: Config = CONFIG) -> List[str]:
    """
    Retrieve a list of DataAccessCommittee object IDs from metadata store.

    Args:
        config: Rumtime configuration

    Returns:
        A list of DataAccessCommittee object IDs.

    """
    client = await get_db_client(config)
    collection = client[config.db_name][COLLECTION_NAME]
    data_access_committees = await collection.find().to_list(None)  # type: ignore
    client.close()
    return [x["id"] for x in data_access_committees]


async def get_data_access_committee(
    data_access_committee_id: str, embedded: bool = False, config: Config = CONFIG
) -> DataAccessCommittee:
    """
    Given a Datset ID, get the DataAccessCommittee object from metadata store.

    Args:
        data_access_committee_id: The DataAccessCommittee ID
        embedded: Whether or not to embed references. ``False``, by default.
        config: Rumtime configuration

    Returns:
        The DataAccessCommittee object

    """
    client = await get_db_client(config)
    collection = client[config.db_name][COLLECTION_NAME]
    data_access_committee = await collection.find_one(
        {"id": data_access_committee_id}
    )  # type: ignore
    if data_access_committee and embedded:
        data_access_committee = await embed_references(
            data_access_committee, config=config
        )
    client.close()
    return data_access_committee
