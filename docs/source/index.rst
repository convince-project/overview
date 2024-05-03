CONVINCE Toolchain Overview
===========================================

Welcome to the CONVINCE toolchain documentation. 
The goal of the `CONVINCE project <https://convince-project.eu/>`_ is to provide an open source toolchain to improve robust robot deliberation with the help of planning, learning, and model checking techniques. 

This is the entry-point for the CONVINCE toolchain documentation. It provides an overview of all the individual components which are part of the large toolchain. Those components can be used standalone and also linked together as required for individual use cases.

The CONVINCE toolchain works as depicted in the picture below. The individual repos and documentations are linked from the picture.

TODO: IMAGE

In the following the components will be briefly described. For more details please check out the individual repositories with their documentation and tutorial pages.

coverage-plan
---------------
To be filled by UoB.

refine-plan
---------------
To be filled by UoB.

active-plan
---------------
To be filled by UoB.

simulate-plan
---------------
To be filled by UoB.

scan
---------------
To be filled by UniGe.

moon
---------------
To be filled by UniGe.

mc-toolchain-jani
---------------
This is a toolbox for converting all specifications of components of a robotic system under investigation into a format which can be given as input to model checkers for verifying the robustness of the system functionalities. The resulting format used for model checking is `JANI <https://jani-spec.org>`_. 

The toolbox consist of a script to convert models describing the system and its environment together, given in the CONVINCE robotics JANI flavor as specified in the `data model repository <https://github.com/convince-project/data-model>`_, into `plain JANI <https://jani-spec.org>`_ accepted as input by model checkers. 
The second part of the provided toolchain components centers around system specifications given in ScXML and how to convert them into a plain Jani file for model checking. This comprises property specification in temporal logic, currently given in Jani, a behavior tree in XML, plugins and nodes in ScXML, and an environment specification in ScXML.

model2code
---------------
To be filled by IIT.

smc-storm
---------------
This is a statistical model checking engine for DTMC models given in Jani, which has been implemented as an extension to the famous `Storm model checker <https://stormchecker.org>`_.



Contents
--------

.. toctree::

   overview
   tutorials
   test
