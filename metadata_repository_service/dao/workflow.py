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
Convenience methods for retrieving Workflow records
"""

from typing import List

from metadata_repository_service.config import CONFIG, Config
from metadata_repository_service.core.utils import embed_references
from metadata_repository_service.dao.db import get_db_client
from metadata_repository_service.models import Workflow

COLLECTION_NAME = "Workflow"


async def retrieve_workflows(config: Config = CONFIG) -> List[str]:
    """
    Retrieve a list of Workflow object IDs from metadata store.

    Returns:
        A list of Workflow object IDs.
        config: Rumtime configuration

    """
    client = await get_db_client(config)
    collection = client[config.db_name][COLLECTION_NAME]
    workflows = await collection.find().to_list(None)  # type: ignore
    client.close()
    return [x["id"] for x in workflows]


async def get_workflow(
    workflow_id: str, embedded: bool = False, config: Config = CONFIG
) -> Workflow:
    """
    Given an Workflow ID, get the Workflow object from metadata store.

    Args:
        workflow_id: The Workflow ID
        embedded: Whether or not to embed references. ``False``, by default.
        config: Rumtime configuration

    Returns:
        The Workflow object

    """
    client = await get_db_client(config)
    collection = client[config.db_name][COLLECTION_NAME]
    workflow = await collection.find_one({"id": workflow_id})  # type: ignore
    if workflow and embedded:
        workflow = await embed_references(workflow, config=config)
    client.close()
    return workflow
