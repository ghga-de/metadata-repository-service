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
"Routes for retrieving Studies"

from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from metadata_repository_service.dao.technology import get_technology
from metadata_repository_service.models import Technology

technology_router = APIRouter()


@technology_router.get(
    "/technologies/{technology_id}",
    response_model=Technology,
    summary="Get a Technology",
)
async def get_technologies(technology_id: str, embedded: bool = False):
    """
    Given a Technology ID, get the Technology record from the metadata store.
    """
    technology = await get_technology(technology_id, embedded)
    if not technology:
        raise HTTPException(
            status_code=404,
            detail=f"{Technology.__name__} with id '{technology_id}' not found",
        )
    return technology
