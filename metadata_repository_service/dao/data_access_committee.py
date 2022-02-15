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
Convenience methods for retrieving DataAccessCommittee records
"""

import random
from typing import List

from metadata_repository_service.config import CONFIG, Config
from metadata_repository_service.core.utils import (
    generate_uuid,
    get_entity,
    get_timestamp,
)
from metadata_repository_service.dao.db import get_db_client
from metadata_repository_service.dao.member import create_member, get_member
from metadata_repository_service.models import (
    CreateDataAccessCommittee,
    DataAccessCommittee,
)

COLLECTION_NAME = "DataAccessCommittee"


async def retrieve_data_access_committees(config: Config = CONFIG) -> List[str]:
    """
    Retrieve a list of DataAccessCommittee object IDs from metadata store.

    Args:
        config: Rumtime configuration

    Returns:
        A list of DataAccessCommittee object IDs.

    """
    client = await get_db_client(config)
    collection = client[config.db_name][COLLECTION_NAME]
    data_access_committees = await collection.find().to_list(None)  # type: ignore
    client.close()
    return [x["id"] for x in data_access_committees]


async def get_data_access_committee(
    data_access_committee_id: str, embedded: bool = False, config: Config = CONFIG
) -> DataAccessCommittee:
    """
    Given a DatsetAccessCommittee ID, get the DataAccessCommittee object
    from metadata store.

    Args:
        data_access_committee_id: The DataAccessCommittee ID
        embedded: Whether or not to embed references. ``False``, by default.
        config: Rumtime configuration

    Returns:
        The DataAccessCommittee object

    """
    data_access_committee = await get_entity(
        identifier=data_access_committee_id,
        field="id",
        collection_name=COLLECTION_NAME,
        embedded=embedded,
        config=config,
    )
    return data_access_committee


async def get_data_access_committee_by_accession(
    data_access_committee_accession: str, embedded: bool = True, config: Config = CONFIG
) -> DataAccessCommittee:
    """
    Given a DataAccessCommittee accession, get the corresponding
    DataAccessCommittee object from metadata store.

    Args:
        data_access_committee_accession: The DataAccessCommittee accession
        embedded: Whether or not to embed references. ``False``, by default.
        config: Rumtime configuration

    Returns:
        The DataAccessCommittee object

    """
    dac = await get_entity(
        identifier=data_access_committee_accession,
        field="accession",
        collection_name=COLLECTION_NAME,
        embedded=embedded,
        config=config,
    )
    return dac


async def create_data_access_committee(
    data_access_committee: CreateDataAccessCommittee, config: Config = CONFIG
) -> DataAccessCommittee:
    """
    Create a DataAccessCommittee object and write to the metadata store.

    Args:
        data_access_committee: The DataAccessCommittee object
        config: Rumtime configuration

    Returns:
        The newly created DataAccessCommittee object

    """
    client = await get_db_client(config)
    collection = client[config.db_name][COLLECTION_NAME]
    member_entity_id_list = []
    member_objs = {
        data_access_committee.main_contact.email: data_access_committee.main_contact
    }
    for member_obj in data_access_committee.has_member:
        member_objs[member_obj.email] = member_obj

    main_contact_member = None
    for member_obj in member_objs.values():
        member = get_member(member_obj["id"], config=config)
        if not member:
            member_entity = await create_member(member_obj)
        if member_entity["email"] == data_access_committee.main_contact.email:
            main_contact_member = member_entity
        member_entity_id_list.append(member_entity["id"])

    dac_entity = data_access_committee.dict()
    dac_entity["id"] = await generate_uuid()
    dac_entity["create_date"] = await get_timestamp()
    dac_entity["update_date"] = dac_entity["create_date"]
    dac_entity["has_member"] = member_entity_id_list
    dac_entity["main_contact"] = main_contact_member["id"]
    dac_entity["accession"] = f"GHGA:DAC000000000{random.randint(1, 999)}"
    await collection.insert_one(dac_entity)
    client.close()
    dac = await get_data_access_committee(dac_entity["id"])
    print(f"> {dac}")
    return dac
