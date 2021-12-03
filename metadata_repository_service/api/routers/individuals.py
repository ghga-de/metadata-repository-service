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
"Routes for retrieving Individuals"

from fastapi import APIRouter

from metadata_repository_service.dao.individual import get_individual
from metadata_repository_service.models import Individual

individual_router = APIRouter()


@individual_router.get(
    "/individuals/{individual_id}",
    response_model=Individual,
    summary="Get a Individual",
)
async def get_individuals(individual_id: str, embedded: bool = False):
    """
    Given a Individual ID, get the Individual record from the metadata store.
    """
    individual = await get_individual(individual_id, embedded)
    return individual
