# Blockchain

Simple blockchain based on Proof of Work consensus mechanism written in Python.
Nodes use TCP protocol to exchange data about current state of the chain.

## Running

To start the node run the command:

```console
python3 run_node.py
```

Private key is loaded from key.pem file (if it exists - otherwise the program generates private keys and creates such a file itself).

## Tests

To run tests run the following command in root project directory:

```console
python3 -m unittest discover -s tests
```
