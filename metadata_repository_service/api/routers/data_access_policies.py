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

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from metadata_repository_service.config import Config, get_config
from metadata_repository_service.dao.data_access_policy import get_data_access_policy
from metadata_repository_service.models import DataAccessPolicy

data_access_policy_router = APIRouter()


@data_access_policy_router.get(
    "/data_access_policies/{data_access_policy_id}",
    response_model=DataAccessPolicy,
    summary="Get a DataAccessPolicy",
)
async def get_data_access_policies(
    data_access_policy_id: str,
    embedded: bool = False,
    config: Config = Depends(get_config),
):
    """
    Given a DataAccessPolicy ID, get the DataAccessPolicy record from the metadata store.
    """
    data_access_policy = await get_data_access_policy(
        data_access_policy_id=data_access_policy_id, embedded=embedded, config=config
    )
    if not data_access_policy:
        raise HTTPException(
            status_code=404,
            detail=f"{DataAccessPolicy.__name__} with id '{data_access_policy_id}' not found",
        )
    return data_access_policy
