#!/usr/bin/env python3
"""
Convenience methods for retrieving Dataset summary
"""
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


from metadata_repository_service.config import CONFIG, Config
from metadata_repository_service.dao.utils import get_entity
from metadata_repository_service.models import Dataset

# pylint: disable=too-many-locals, too-many-statements, too-many-branches
COLLECTION_NAME = "Dataset"


async def get_dataset_for_summary_object(
    dataset_id: str, config: Config = CONFIG
) -> Dataset:
    """
    Given a Dataset ID, get the Dataset object from metadata store.

    Args:
        dataset_id: The Dataset ID
        embedded: Whether or not to embed references. ``False``, by default.
        config: Rumtime configuration

    Returns:
        The Dataset object

    """
    dataset = await get_entity(
        identifier=dataset_id,
        field="id",
        collection_name=COLLECTION_NAME,
        model_class=Dataset,
        embedded=True,
        config=config,
    )
    return dataset
