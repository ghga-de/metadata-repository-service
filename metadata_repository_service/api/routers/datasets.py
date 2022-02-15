# Copyright 2021 - 2022 Universität Tübingen, DKFZ and EMBL
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

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from metadata_repository_service.api.deps import get_config
from metadata_repository_service.config import Config
from metadata_repository_service.dao.data_access_policy import (
    get_data_access_policy_by_accession,
)
from metadata_repository_service.dao.dataset import create_dataset, get_dataset
from metadata_repository_service.dao.file import get_file_by_accession
from metadata_repository_service.models import (
    CreateDataset,
    Dataset,
    DatasetStatusPatch,
)

dataset_router = APIRouter()


@dataset_router.get(
    "/datasets/{dataset_id}",
    response_model=Dataset,
    summary="Get a Dataset",
    tags=["Query"],
)
async def get_datasets(
    dataset_id: str, embedded: bool = False, config: Config = Depends(get_config)
):
    """
    Given a Dataset ID, get the Dataset record from the metadata store.
    """
    dataset = await get_dataset(dataset_id=dataset_id, embedded=embedded, config=config)
    if not dataset:
        raise HTTPException(
            status_code=404,
            detail=f"{Dataset.__name__} with id '{dataset_id}' not found",
        )
    return dataset


@dataset_router.post(
    "/datasets", response_model=Dataset, summary="Create a Dataset", tags=["Dataset"]
)
async def create_datasets(dataset: CreateDataset, config: Config = Depends(get_config)):
    """
    Given a list of File accessions and a DataAccessPolicy accession, create a
    Dataset and write to the metadata store.
    """
    dap_accession = dataset.has_data_access_policy
    dap_entity = await get_data_access_policy_by_accession(dap_accession, config=config)
    if not dap_entity:
        raise HTTPException(
            status_code=404,
            detail=f"DataAccessPolicy Accession {dap_accession} provided in "
            + "'dataset.has_data_access_policy' could not be found. "
            + "Cannot create a Dataset that references a "
            + "non-existing DataAccessPolicy.",
        )

    file_accessions = dataset.has_file
    for file_accession in file_accessions:
        file_entity = await get_file_by_accession(file_accession, config=config)
        if not file_entity:
            raise HTTPException(
                status_code=404,
                detail=f"File Accession {file_accession} provided in "
                + "'dataset.has_file' could not be found. "
                + "Cannot create a Dataset that references a "
                + "non-existing File entity.",
            )

    dataset = await create_dataset(dataset, config=config)
    return dataset


@dataset_router.post(
    "/datasets/{dataset_id}",
    response_model=Dataset,
    summary="Update status of a Dataset",
    tags=["Dataset"],
)
async def update_dataset_status(dataset_id: str, dataset: DatasetStatusPatch):
    """
    Update status of a Dataset entity.
    """
    pass
