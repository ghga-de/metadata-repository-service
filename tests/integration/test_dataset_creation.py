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
"""Test the creation of dataset via the API"""

import nest_asyncio

from ..fixtures.mongodb import MongoAppFixture, mongo_app_fixture2  # noqa: F401

nest_asyncio.apply()


def test_create_dataset(mongo_app_fixture2: MongoAppFixture):  # noqa: F811
    """Test creation of a Dataset"""
    client = mongo_app_fixture2.app_client
    dac_data = {
        "name": "Test DAC",
        "description": "A Data Access Committee for sharing test datasets",
        "main_contact": {
            "organization": "GHGA",
            "email": "foo@ghga.de",
        },
        "has_member": [
            {
                "organization": "GHGA",
                "email": "foo@ghga.de",
            },
            {"organization": "GHGA", "email": "bar@ghga.de"},
        ],
    }
    response = client.post("/data_access_committees", json=dac_data)
    dac_entity = response.json()
    assert "accession" in dac_entity
    dac_accession = dac_entity["accession"]
    assert dac_accession

    dap_data = {
        "name": "New DAP",
        "policy_text": "Some text that explains the access restrictions",
        "has_data_access_committee": dac_accession,
    }
    response = client.post("/data_access_policies", json=dap_data)
    dap_entity = response.json()
    assert "accession" in dap_entity
    dap_accession = dap_entity["accession"]
    assert dap_accession

    dataset_data = {
        "has_file": ["GHGA:FIL000000000001", "GHGA:FIL000000000002"],
        "has_data_access_policy": dap_accession,
    }
    response = client.post("/datasets", json=dataset_data)
    dataset_entity = response.json()
    assert "accession" in dataset_entity
    dataset_accession = dataset_entity["accession"]
    assert dataset_accession
    assert len(dataset_data["has_file"]) == len(dataset_entity["has_file"])
    assert dap_entity["id"] == dataset_entity["has_data_access_policy"]

    response = client.get(f"/datasets/{dataset_entity['id']}?embedded=true")
    full_dataset_entity = response.json()
    assert "has_file" in full_dataset_entity
    assert len(full_dataset_entity["has_file"]) == 2
    assert "has_experiment" in full_dataset_entity
    assert len(full_dataset_entity["has_experiment"]) == 2
    assert "has_sample" in full_dataset_entity
    assert len(full_dataset_entity["has_sample"]) == 1
    assert "has_study" in full_dataset_entity
    assert len(full_dataset_entity["has_study"]) == 1
    assert "status" in full_dataset_entity
    assert full_dataset_entity["status"] == "unreleased"

    dataset_patch = {"status": "released"}
    response = client.patch(
        f"/datasets/{full_dataset_entity['accession']}", json=dataset_patch
    )
    patched_dataset = response.json()
    assert patched_dataset["status"] == dataset_patch["status"]
    assert patched_dataset["creation_date"] != patched_dataset["update_date"]
