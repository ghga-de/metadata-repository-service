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
"Routes for retrieving DataAccessCommittees"

from typing import List

from fastapi import APIRouter

from metadata_repository_service.dao.data_access_committee import (
    get_data_access_committee,
    retrieve_data_access_committees,
)
from metadata_repository_service.models import DataAccessCommittee

data_access_committee_router = APIRouter()


@data_access_committee_router.get(
    "/data_access_committees",
    response_model=List[str],
    summary="Get all DataAccessCommittee IDs",
)
async def get_all_data_access_committees():
    """
    Retrieve a list of DataAccessCommittee IDs from the metadata store.
    """
    data_access_committees = await retrieve_data_access_committees()
    return data_access_committees


@data_access_committee_router.get(
    "/data_access_committees/{data_access_committee_id}",
    response_model=DataAccessCommittee,
    summary="Get a DataAccessCommittee",
)
async def get_data_access_committees(
    data_access_committee_id: str, embedded: bool = False
):
    """
    Given a DataAccessCommittee ID, get the DataAccessCommittee record from the metadata store.
    """
    data_access_committee = await get_data_access_committee(
        data_access_committee_id, embedded
    )
    return data_access_committee
