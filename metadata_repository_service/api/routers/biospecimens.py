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
"Routes for retrieving Biospecimens"

from typing import List

from fastapi import APIRouter

from metadata_repository_service.dao.biospecimen import (
    get_biospecimen,
    retrieve_biospecimens,
)
from metadata_repository_service.models import Biospecimen

biospecimen_router = APIRouter()


@biospecimen_router.get(
    "/biospecimens", response_model=List[str], summary="Get all Biospecimen IDs"
)
async def get_all_biospecimens():
    """
    Retrieve a list of Biospecimen IDs from the metadata store.
    """
    biospecimens = await retrieve_biospecimens()
    return biospecimens


@biospecimen_router.get(
    "/biospecimens/{biospecimen_id}",
    response_model=Biospecimen,
    summary="Get a Biospecimen",
)
async def get_biospecimens(biospecimen_id: str, embedded: bool = False):
    """
    Given a Biospecimen ID, get the Biospecimen record from the metadata store.
    """
    biospecimen = await get_biospecimen(biospecimen_id, embedded)
    return biospecimen
