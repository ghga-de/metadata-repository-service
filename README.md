![tests](https://github.com/ghga-de/metadata-service/actions/workflows/unit_and_int_tests.yaml/badge.svg)
[![codecov](https://codecov.io/gh/ghga-de/metadata-service/branch/main/graph/badge.svg?token=GYH99Y71CK)](https://codecov.io/gh/ghga-de/microservice-repository-template)

# GHGA Metadata Service

The GHGA Metadata Service is a service that is responsible for reading from and writing to the Metadata Store.
It provides an API layer on top of the Metadata Store.

The service is also responsible for validating the incoming metadata JSON and ensuring that the metadata records
are conformant to the [GHGA Metadata Schema](https://github.com/ghga-de/ghga-metadata-schema).

The service may communicate with other services to facilitate metadata management.
