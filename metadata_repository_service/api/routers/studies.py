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

from typing import List

from fastapi import APIRouter

from metadata_repository_service.dao.study import get_study, retrieve_studies
from metadata_repository_service.models import Study

study_router = APIRouter()


@study_router.get("/studies", response_model=List[str], summary="Get all Study IDs")
async def get_all_studies():
    """
    Retrieve a list of Study IDs from the metadata store.
    """
    studies = await retrieve_studies()
    return studies


@study_router.get(
    "/studies/{study_id}",
    response_model=Study,
    summary="Get a Study",
)
async def get_studies(study_id: str, embedded: bool = False):
    """
    Given a Study ID, get the Study record from the metadata store.
    """
    study = await get_study(study_id, embedded)
    return study
