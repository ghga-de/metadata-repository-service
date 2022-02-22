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
Core uilities for the functionality of Metadata Repository Service.
"""
import copy
import datetime
import logging
import random
import uuid
from typing import Any, Dict, Set

import stringcase

from metadata_repository_service.config import CONFIG, Config
from metadata_repository_service.dao.db import get_db_client

# pylint: disable=too-many-arguments

embedded_fields: Set = {
    "analysis",
    "analysis_process",
    "biospecimen",
    "data_access_committee",
    "data_access_policy",
    "dataset",
    "experiment_process",
    "experiment",
    "file",
    "individual",
    "member",
    "project",
    "protocol",
    "publication",
    "sample",
    "study",
    "technology",
    "workflow",
}


async def _get_reference(
    document_id: str, collection_name: str, config: Config = CONFIG
) -> Dict:
    """Given a document ID and a collection name, query the metadata store
    and return the document.

    Args:
        document_id: The ID of the document
        collection_name: The collection in the metadata store that has the document

    Returns
        The document corresponding to ``document_id``

    """
    client = await get_db_client(config)
    collection = client[config.db_name][collection_name]
    doc = await collection.find_one({"id": document_id})  # type: ignore
    if not doc:
        logging.warning(
            "Reference with ID %s not found in collection %s",
            document_id,
            collection_name,
        )
    return doc


async def get_entity(
    identifier: str,
    field: str,
    collection_name: str,
    model_class: Any = None,
    embedded: bool = False,
    config: Config = CONFIG,
) -> Any:
    """
    Given an identifier, field name and collection name, look up the
    identifier in the provided field of a collection and return the
    corresponding document.

    Args:
        identifier: The identifier
        field: The name of the field
        collection_name: The collection in the metadata store that has the document
        model_class:
        embedded: Whether or not to embed references. ``False``, by default.
        config: Rumtime configuration

    Returns
        The document

    """
    client = await get_db_client(config)
    collection = client[config.db_name][collection_name]
    entity = await collection.find_one({field: identifier})  # type: ignore
    if entity and embedded:
        entity = await embed_references(entity, config=config)
    client.close()
    if model_class and entity:
        entity_obj = model_class(**entity)
    else:
        entity_obj = entity
    return entity_obj


async def embed_references(document: Dict, config: Config = CONFIG) -> Dict:
    """Given a document and a document type, identify the references in ``document``
    and query the metadata store. After retrieving the referenced objects,
    embed them in place of the reference in the parent document.

    Args:
        document: The document that has one or more references

    Returns
        The denormalize/embedded document

    """
    parent_document = copy.deepcopy(document)
    for field in parent_document.keys():
        if field.startswith("has_") and field not in {"has_attribute"}:
            cname = field.split("_", 1)[1]
            if cname not in embedded_fields:
                continue
            formatted_cname = stringcase.pascalcase(cname)
            if isinstance(parent_document[field], str):
                referenced_doc = await _get_reference(
                    parent_document[field], formatted_cname, config=config
                )
                if referenced_doc:
                    referenced_doc = await embed_references(
                        referenced_doc, config=config
                    )
                    parent_document[field] = referenced_doc
            elif isinstance(parent_document[field], (list, set, tuple)):
                docs = []
                for ref in parent_document[field]:
                    referenced_doc = await _get_reference(
                        ref, formatted_cname, config=config
                    )
                    if referenced_doc:
                        referenced_doc = await embed_references(
                            referenced_doc, config=config
                        )
                        docs.append(referenced_doc)
                if docs:
                    parent_document[field] = docs
    return parent_document


async def get_timestamp() -> str:
    """
    Get the current timestamp in UTC according to ISO 8601

    Returns:
        The timestamp as a string

    """
    return datetime.datetime.utcnow().isoformat()


async def generate_uuid() -> str:
    """
    Generate a UUID.

    Returns:
        A new UUID

    """
    return str(uuid.uuid4())


async def generate_accession(collection_name: str, config: Config = CONFIG) -> str:
    """
    Generate a unique accession.

    The uniqueness of the accession is ensured by checking the metadata store
    to see if a generated accession already exists.

    Args:
        collection_name: The name of the collection
        config: Runtime configuration

    Returns:
        A new accession

    """
    client = await get_db_client(config)
    collection = client[config.db_name]["_accession_tracker_"]
    accession = await _generate_accession(collection_name=collection_name)
    accession_tracker_obj = await collection.find_one({"accession": accession})  # type: ignore
    if accession_tracker_obj:
        accession = await generate_accession(
            collection_name=collection_name, config=config
        )
    else:
        accession_tracker_obj = {
            "accession": accession,
            "timestamp": await get_timestamp(),
        }
        await collection.insert_one(accession_tracker_obj)
    client.close()
    return accession


async def _generate_accession(collection_name: str) -> str:
    """
    Generate an accession for a collection.

    Args:
        collection_name: The name of the collection

    Returns:
        A new accession

    """
    special_accession_prefix = {
        "DataAccessPolicy": "DAP",
        "DataAccessCommittee": "DAC",
    }
    reference = random.randint(1, 999_999_999_999)  # nosec
    if collection_name in special_accession_prefix:
        collection_abbr = special_accession_prefix.get(collection_name)
    else:
        collection_abbr = collection_name[:3].upper()
    accession = f"GHGA:{collection_abbr}{str(reference).zfill(12)}"
    return accession
