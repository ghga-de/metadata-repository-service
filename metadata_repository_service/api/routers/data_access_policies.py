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
"Routes for retrieving DataAccessPolicys"

from typing import List

from fastapi import APIRouter

from metadata_repository_service.dao.data_access_policy import (
    get_data_access_policy,
    retrieve_data_access_policies,
)
from metadata_repository_service.models import DataAccessPolicy

data_access_policy_router = APIRouter()


@data_access_policy_router.get(
    "/data_access_policies",
    response_model=List[str],
    summary="Get all DataAccessPolicy IDs",
)
async def get_all_data_access_policies():
    """
    Retrieve a list of DataAccessPolicy IDs from the metadata store.
    """
    data_access_policies = await retrieve_data_access_policies()
    return data_access_policies


@data_access_policy_router.get(
    "/data_access_policies/{data_access_policy_id}",
    response_model=DataAccessPolicy,
    summary="Get a DataAccessPolicy",
)
async def get_data_access_policies(data_access_policy_id: str, embedded: bool = False):
    """
    Given a DataAccessPolicy ID, get the DataAccessPolicy record from the metadata store.
    """
    data_access_policy = await get_data_access_policy(data_access_policy_id, embedded)
    return data_access_policy
