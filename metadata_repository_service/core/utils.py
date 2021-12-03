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
"""
Core uilities for the functionality of Metadata Repository Service.
"""
import copy
import datetime
import logging
import uuid
from typing import Dict, Set

import stringcase

from metadata_repository_service.config import get_config
from metadata_repository_service.dao.db import get_db_client

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


async def _get_reference(document_id: str, collection_name: str) -> Dict:
    """Given a document ID and a collection name, query the metadata store
    and return the document.

    Args:
        document_id: The ID of the document
        collection_name: The collection in the metadata store that has the document

    Returns
        The document corresponding to ``document_id``

    """
    client = await get_db_client()
    config = get_config()
    collection = client[config.db_name][collection_name]
    doc = await collection.find_one({"id": document_id})  # type: ignore
    if not doc:
        logging.warning(
            "Reference with ID %s not found in collection %s",
            document_id,
            collection_name,
        )
    return doc


async def embed_references(document: Dict) -> Dict:
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
                    parent_document[field], formatted_cname
                )
                if referenced_doc:
                    referenced_doc = await embed_references(referenced_doc)
                    parent_document[field] = referenced_doc
            elif isinstance(parent_document[field], (list, set, tuple)):
                docs = []
                for ref in parent_document[field]:
                    referenced_doc = await _get_reference(ref, formatted_cname)
                    if referenced_doc:
                        referenced_doc = await embed_references(referenced_doc)
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
