# Epistemic Me Python SDK

From this folder, you can run:

``` bash
make install
make generate-proto
```

The `make install` command will install the dependencies and the `make generate-proto` command will generate the Python classes from the proto files.

To run the tests, you can run:

``` bash
make test
```

Or you can run the tests with the following command:

``` bash
pytest tests/test_grpc_client.py
```

To run the tests against a local server, you can run:

``` bash
pytest tests/test_self_model_grpc.py
```
