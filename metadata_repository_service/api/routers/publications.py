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
"Routes for retrieving Publications"

from fastapi import APIRouter

from metadata_repository_service.dao.publication import get_publication
from metadata_repository_service.models import Publication

publication_router = APIRouter()


@publication_router.get(
    "/publications/{publication_id}",
    response_model=Publication,
    summary="Get a Publication",
)
async def get_publications(publication_id: str, embedded: bool = False):
    """
    Given a Publication ID, get the Publication record from the metadata store.
    """
    publication = await get_publication(publication_id, embedded)
    return publication
