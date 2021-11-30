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
Convenience methods for adding, updating, and retrieving Dataset records
"""

from typing import List

from fastapi.exceptions import HTTPException

from metadata_repository_service.config import get_config
from metadata_repository_service.dao.db import get_db_client
from metadata_repository_service.models import Dataset

COLLECTION_NAME = "Dataset"

config = get_config()


async def retrieve_datasets() -> List[Dataset]:
    """
    Retrieve a list of Dataset objects from metadata store.

    Returns:
        A list of Dataset objects.

    """
    client = await get_db_client()
    collection = client[config.db_name][COLLECTION_NAME]
    datasets = await collection.find().to_list(None)  # type: ignore
    client.close()
    return datasets


async def get_dataset(dataset_id: str) -> Dataset:
    """
    Given a Datset ID, get the Dataset object from metadata store.

    Args:
        dataset_id: The Dataset ID

    Returns:
        The Dataset object

    """
    client = await get_db_client()
    collection = client[config.db_name][COLLECTION_NAME]
    dataset = await collection.find_one({"id": dataset_id})  # type: ignore
    if not dataset:
        raise HTTPException(
            status_code=404,
            detail=f"{Dataset.__name__} with id '{dataset_id}' not found",
        )
    client.close()
    return dataset
