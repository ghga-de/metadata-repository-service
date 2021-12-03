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
Convenience methods for retrieving Dataset records
"""

from typing import List

from metadata_repository_service.config import Config, get_config
from metadata_repository_service.core.utils import embed_references
from metadata_repository_service.dao.db import get_db_client
from metadata_repository_service.models import Dataset

COLLECTION_NAME = "Dataset"


async def retrieve_datasets(config: Config = get_config()) -> List[str]:
    """
    Retrieve a list of Dataset object IDs from metadata store.

    Args:
        config: Rumtime configuration

    Returns:
        A list of Dataset object IDs.

    """
    client = await get_db_client(config.db_url)
    collection = client[config.db_name][COLLECTION_NAME]
    datasets = await collection.find().to_list(None)  # type: ignore
    client.close()
    return [x["id"] for x in datasets]


async def get_dataset(
    dataset_id: str, embedded: bool = False, config: Config = get_config()
) -> Dataset:
    """
    Given a Datset ID, get the Dataset object from metadata store.

    Args:
        dataset_id: The Dataset ID
        embedded: Whether or not to embed references. ``False``, by default.
        config: Rumtime configuration

    Returns:
        The Dataset object

    """
    client = await get_db_client(config.db_url)
    collection = client[config.db_name][COLLECTION_NAME]
    dataset = await collection.find_one({"id": dataset_id})  # type: ignore
    if dataset and embedded:
        dataset = await embed_references(dataset)
    client.close()
    return dataset
