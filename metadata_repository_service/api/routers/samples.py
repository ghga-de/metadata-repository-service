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
"Routes for retrieving Samples"

from fastapi import APIRouter

from metadata_repository_service.dao.sample import get_sample
from metadata_repository_service.models import Sample

sample_router = APIRouter()


@sample_router.get(
    "/samples/{sample_id}",
    response_model=Sample,
    summary="Get a Sample",
)
async def get_samples(sample_id: str, embedded: bool = False):
    """
    Given a Sample ID, get the Sample record from the metadata store.
    """
    sample = await get_sample(sample_id, embedded)
    return sample
