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
Convenience methods for retrieving Submission records
"""

from typing import List

from pymongo import ReturnDocument

from metadata_repository_service.config import CONFIG, Config
from metadata_repository_service.core.utils import embed_references
from metadata_repository_service.dao.db import get_db_client
from metadata_repository_service.models import Submission

COLLECTION_NAME = "Submission"


async def retrieve_submissions(config: Config = CONFIG) -> List[str]:
    """
    Retrieve a list of Submission object IDs from metadata store.

    Args:
        config: Rumtime configuration

    Returns:
        A list of Submission object IDs.

    """
    client = await get_db_client(config)
    collection = client[config.db_name][COLLECTION_NAME]
    submissions = await collection.find().to_list(None)  # type: ignore
    client.close()
    return [x["id"] for x in submissions]


async def get_submission(
    submission_id: str, embedded: bool = False, config: Config = CONFIG
) -> Submission:
    """
    Given a Submission ID, get the Submission object from metadata store.

    Args:
        submission_id: The Submission ID
        embedded: Whether or not to embed references. ``False``, by default.
        config: Rumtime configuration

    Returns:
        The Submission object

    """
    client = await get_db_client(config)
    collection = client[config.db_name][COLLECTION_NAME]
    submission = await collection.find_one({"id": submission_id})  # type: ignore
    if submission and embedded:
        submission = await embed_references(submission, config=config)
    client.close()
    return Submission(**submission)


async def insert_submission(submission: Submission, config: Config = CONFIG):
    """
    Store a Submission object into metadata store.

    Args:
        submission: Submission object
        config: Rumtime configuration

    """
    client = await get_db_client(config)
    collection = client[config.db_name][COLLECTION_NAME]
    await collection.insert_one(submission)
    client.close()


async def update_submission_status(
    submission_id: str, status_value: str, config: Config = CONFIG
) -> Submission:
    """
    Updates a Submission object status.

    Args:
        submission: Submission object
        config: Rumtime configuration

    """
    client = await get_db_client(config)
    collection = client[config.db_name][COLLECTION_NAME]
    submission = await collection.find_one_and_update(
        {"id": submission_id},
        {"$set": {"status": status_value}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    client.close()

    return submission
