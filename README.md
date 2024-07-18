# xApp Development from Zero to Hero: Online Resources

This repository provides online resources to support xApp development for managing O-RAN networks. It provides xApp developers with example configuration files, source code for xApps in Python, representation of ASN.1 data structures in Python, and a cheat sheet of useful commands. 
 
Please see the repository structure below:

1. [Example configuration files](/configuration_files/) (xApp descriptor, schema, static RMR route file, and Dockerfile)
2. [Example source codes](/source_code/) (including both RMRXApp and XApp implementations)
3. [Python representations of ASN.1](/asn1/) (from the E2AP, E2SM, and KPM specifications)
4. [Command cheatsheet](/example_commands/) (for Docker, Kubernetes, and dms_cli to interface with the AppMgr)

Each link provides additional information about the specific resources. (WIP)


This repository serves as a companion to our tutorial paper:
> Joao F. Santos, Alexandre Huff, Daniel Campos, Kleber V. Cardoso, Cristiano B. Both, and Luiz A.
DaSilva, “Managing O-RAN Networks: xApp Development from Zero to Hero”, publicly available on arXiv
preprint arXiv:2407.09619, 2024.

For more information and context about this repository and the online resources therein, check our preprint manuscript on ArXiv: [https://arxiv.org/abs/2407.09619](https://arxiv.org/abs/2407.09619).

Note that we leverage the Python xApp Framework from the [O-RAN Software Community](https://o-ran-sc.org/) to develop xApps. For more information about it, please check its [official documentation](https://docs.o-ran-sc.org/projects/o-ran-sc-ric-plt-xapp-frame-py/en/latest/).
In addition, we leverage PyCrate to create the representations of ASN.1 in Python. For information and examples about it, please check its [official repository](https://github.com/pycrate-org/pycrate).

## Credits
- Alexandre Huff (UTFPR)
- Cristiano Bonato Both (UNISINOS)
- Daniel Campos(UFG)
- João F. Santos (Virginia Tech)
- Kleber V. Cardoso (UFG)
- Luiz A. DaSilva (Virginia Tech)
