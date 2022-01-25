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
Convenience methods for retrieving AnalysisProcess records
"""

from typing import List

from metadata_repository_service.config import CONFIG, Config
from metadata_repository_service.core.utils import embed_references
from metadata_repository_service.dao.db import get_db_client
from metadata_repository_service.models import AnalysisProcess

COLLECTION_NAME = "AnalysisProcess"


async def retrieve_analysis_processes(config: Config = CONFIG) -> List[str]:
    """
    Retrieve a list of AnalysisProcess objects from metadata store.

    Args:
        config: Rumtime configuration

    Returns:
        A list of AnalysisProcess object IDs.

    """
    client = await get_db_client(config)
    collection = client[config.db_name][COLLECTION_NAME]
    analysis_processes = await collection.find_distinct().to_list(None)  # type: ignore
    client.close()
    return [x["id"] for x in analysis_processes]


async def get_analysis_process(
    analysis_process_id: str, embedded: bool = True, config: Config = CONFIG
) -> AnalysisProcess:
    """
    Given a Datset ID, get the AnalysisProcess object from metadata store.

    Args:
        analysis_process_id: The AnalysisProcess ID
        embedded: Whether or not to embed references. ``False``, by default.
        config: Rumtime configuration

    Returns:
        The AnalysisProcess object

    """
    client = await get_db_client(config)
    collection = client[config.db_name][COLLECTION_NAME]
    analysis_process = await collection.find_one({"id": analysis_process_id})  # type: ignore
    if analysis_process and embedded:
        analysis_process = await embed_references(analysis_process, config=config)
    client.close()
    return analysis_process
