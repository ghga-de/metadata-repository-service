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
"""
Convenience methods for retrieving Dataset records
"""

from typing import List

from metadata_repository_service.api.routers.studies import get_studies
from metadata_repository_service.config import CONFIG, Config
from metadata_repository_service.core.utils import (
    embed_references,
    generate_uuid,
    get_entity,
    get_timestamp,
)
from metadata_repository_service.dao.analysis import get_analysis_by_linked_files
from metadata_repository_service.dao.data_access_policy import (
    get_data_access_policy_by_accession,
)
from metadata_repository_service.dao.db import get_db_client
from metadata_repository_service.dao.experiment import get_experiment_by_linked_files
from metadata_repository_service.dao.file import get_file_by_accession
from metadata_repository_service.dao.sample import get_sample
from metadata_repository_service.dao.study import get_study
from metadata_repository_service.models import CreateDataset, Dataset

COLLECTION_NAME = "Dataset"


async def retrieve_datasets(config: Config = CONFIG) -> List[str]:
    """
    Retrieve a list of Dataset object IDs from metadata store.

    Args:
        config: Rumtime configuration

    Returns:
        A list of Dataset object IDs.

    """
    client = await get_db_client(config)
    collection = client[config.db_name][COLLECTION_NAME]
    datasets = await collection.find().to_list(None)  # type: ignore
    client.close()
    return [x["id"] for x in datasets]


async def get_dataset(
    dataset_id: str, embedded: bool = False, config: Config = CONFIG
) -> Dataset:
    """
    Given a Dataset ID, get the Dataset object from metadata store.

    Args:
        dataset_id: The Dataset ID
        embedded: Whether or not to embed references. ``False``, by default.
        config: Rumtime configuration

    Returns:
        The Dataset object

    """
    dataset = get_entity(
        identifier=dataset_id,
        field="id",
        collection_name=COLLECTION_NAME,
        embedded=embedded,
        config=config,
    )
    return dataset


async def create_dataset(dataset: CreateDataset, config: Config = CONFIG) -> Dataset:
    """
    Given a list of File IDs and a Data Access Policy ID, create a new Dataset object
    and write to the metadata store.

    Args:
        dataset: The Dataset object
        config: Rumtime configuration

    Returns:
        The Dataset object

    """
    client = await get_db_client(config)
    collection = client[config.db_name][COLLECTION_NAME]
    # Get referenced File entities
    file_entities = {}
    for file_accession in dataset.has_file:
        file_entity = get_file_by_accession(
            file_accession=file_accession, config=config
        )
        if not file_entity:
            raise Exception("Cannot find a File with accession: " + file_accession)
        file_entities[file_entity["id"]] = file_entity

    print(f"File objects: {file_entities}")
    dap_entity = await get_data_access_policy_by_accession(
        dataset.has_data_access_policy
    )
    if not dap_entity:
        raise Exception(
            "Cannot find a DataAccessPolicy with accession: "
            + dataset.has_data_access_policy
        )
    file_entity_id_list = list(file_entities.keys())
    print(file_entity_id_list)

    experiment_entities = await get_experiment_by_linked_files(
        file_id_list=file_entity_id_list, config=config
    )
    print(experiment_entities)

    # Get Sample entities that are linked to Experiment entities
    study_entities = {}
    sample_entities = {}
    for experiment in experiment_entities:
        study_entity = await get_study(experiment["has_study"], config=config)
        study_entities[study_entity["id"]] = study_entity
        sample_entity = await get_sample(experiment["has_sample"], config=config)
        sample_entities[sample_entity["id"]] = sample_entity

    # Analysis
    analysis_entities = await get_analysis_by_linked_files(
        file_id_list=file_entity_id_list, config=config
    )
    for analysis in analysis_entities:
        study_entity = await get_study(analysis["has_study"], config=config)
        if study_entity["id"] not in study_entities:
            study_entities[study_entity["id"]] = study_entity

    print(f"Studies: {study_entities}")
    print(f"Samples: {sample_entities}")
    print(f"Analyses: {analysis_entities}")

    # Dataset
    dataset_entity = dataset.dict()
    dataset_entity["id"] = await generate_uuid()
    dataset_entity["creation_date"] = await get_timestamp()
    dataset_entity["update_date"] = dataset_entity["creation_date"]

    dataset_entity["has_file"] = file_entity_id_list
    dataset_entity["has_experiment"] = [x["id"] for x in experiment_entities]
    dataset_entity["has_analysis"] = [x["id"] for x in analysis_entities]
    dataset_entity["has_study"] = list(study_entities.keys())
    dataset_entity["has_sample"] = list(sample_entities.keys())
    dataset_entity["has_data_access_policy"] = dap_entity["id"]

    await collection.insert_one(dataset_entity)
    dataset = await get_dataset(dataset_entity["id"])
    return dataset
