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
"Routes for retrieving Datasets"

from fastapi import APIRouter

from metadata_repository_service.dao.dataset import get_dataset
from metadata_repository_service.models import Dataset

dataset_router = APIRouter()


@dataset_router.get(
    "/datasets/{dataset_id}", response_model=Dataset, summary="Get a Dataset"
)
async def get_datasets(dataset_id: str, embedded: bool = False):
    """
    Given a Dataset ID, get the Dataset record from the metadata store.
    """
    dataset = await get_dataset(dataset_id, embedded)
    return dataset
