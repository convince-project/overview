# CONVINCE Toolchain Overview

> Please access this documentation via [convince-project.github.io/overview](https://convince-project.github.io/overview/)

Welcome to the CONVINCE toolchain documentation. 
The goal of the [CONVINCE project](http://convince-project.eu) is to provide an open source toolchain to improve robust robot deliberation with the help of planning, learning, and verification techniques. 

This is the entry-point for the CONVINCE toolchain documentation. It provides an overview of all the individual components which are part of the large toolchain. Those components can be used standalone and also linked together as required for individual use cases.




## Build documentation

To build the documentation page, `plantuml` needs to be installed to generate the interactive overview picture.
Please download version `v1.2024.4` and move it to the correct location:

```bash
wget https://github.com/plantuml/plantuml/releases/download/v1.2024.4/plantuml-bsd-1.2024.4.jar
mkdir -p /usr/share/plantuml
sudo mv plantuml-bsd-1.2024.4.jar /usr/share/plantuml/plantuml.jar 
```

Then the following command needs to be run to build the documentation:

```bash
cd <path-to-convince_toolchain>/docs
pip install -r requirements.txt
make html
```

It have been tested with Python 3.8.10 and pip version 24.0.
