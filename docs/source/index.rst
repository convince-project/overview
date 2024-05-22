CONVINCE Toolchain Overview
===========================


Welcome to the CONVINCE toolchain documentation. 
The goal of the `CONVINCE project <https://convince-project.eu/>`_ is to provide an open source toolchain to improve robust robot deliberation with the help of planning, learning, and model checking techniques. 

This is the entry-point for the CONVINCE toolchain documentation. It provides an overview of all the individual components which are part of the large toolchain. Those components can be used standalone and also linked together as required for individual use cases.

.. uml::  overview.plantuml
   :caption: CONVINCE Toolchain Overview
   :alt: CONVINCE Toolchain Overview

The CONVINCE toolchain works as depicted above. The individual repos and documentations are linked from there.

In the following the CONVINCE toolchain components are briefly described. For more details please check out the individual repositories with their documentation and tutorial pages.

sit-aw
------
`convince-project/sit-aw <https:///github.com/convince-project/sit-aw>`_

To be filled by CEA.


coverage-plan
-------------
`convince-project/coverage-plan <https:///github.com/convince-project/coverage-plan>`_

.. .. uml::

..    agent "\nSkill Layer\n" as rskill #LightYellow

..    agent coverageplan #PaleGreen [
..    [[https:///github.com/convince-project/coverage-plan COVERAGE-PLAN]]
..    ....
..    WP3 / UoB
..    ]

..    rskill . coverageplan


COVERAGE-PLAN is an online tool for *lifelong area coverage in dynamic and uncertain environments*.

The current release of COVERAGE-PLAN operates on discrete grid environments. 
COVERAGE-PLAN has two components: an online coverage planner, and a learned model of stochastic occupancy dynamics.
The dynamics model `captures the probability that a grid cell becomes occupied or free in the next timestep <https://ieeexplore.ieee.org/abstract/document/6385629>`_.
This model is learned over the robot's lifespan, where the model is updated after each coverage run using the robot's latest observations.
The online coverage planner uses the learned model to build and solve a `partially observable Markov decision process (POMDP) <https://www.sciencedirect.com/science/article/pii/S000437029800023X?via%3Dihub>`_ for area coverage.
The state-of-the-art `DESPOT <https://github.com/AdaCompNUS/despot>`_ algorithm is used to solve POMDPs.
Before deployment, the user must specify the map dimensions, the robot's starting position, the robot's field of view, and the time bound on coverage.

COVERAGE-PLAN can be found `here <https://github.com/convince-project/coverage-plan>`__ and its documentation can be found `here <https://convince-project.github.io/coverage-plan>`__.
The documentation contains a tutorial demonstrating the coverage planner.


refine-plan
-----------
`convince-project/refine-plan <https:///github.com/convince-project/refine-plan>`_

REFINE-PLAN is an offline tool for *refining hand-designed behaviour trees (BTs)* to attain robustness under uncertainty, improving performance.


Behaviour trees are input/output in the XML format defined in `BehaviorTree.cpp v3.8 <https://www.behaviortree.dev>`_.
REFINE-PLAN extracts a state space from the hand-designed BT, and learns probabilistic `options <https://www.sciencedirect.com/science/article/pii/S0004370299000521>`_ in simulation which describe the execution of each action node.
This simulation is provided by the user.
State space extraction and option learning are not implemented in the current release.
Given option set and extracted state space, REFINE-PLAN constructs a `semi-MDP <https://www.sciencedirect.com/science/article/pii/S0004370299000521>`_ and solves it using `Storm/Stormpy <https://moves-rwth.github.io/stormpy/>`_ to synthesise a policy.
This policy is then converted back to a BT using `existing methods <https://ieeexplore.ieee.org/document/10105979>`_.


REFINE-PLAN can be found `here <https://github.com/convince-project/refine-plan>`__ and its documentation can be found `here <https://convince-project.github.io/refine-plan>`__.
The documentation contains a tutorial demonstrating the current functionality.

active-plan
-----------
`convince-project/active-plan <https:///github.com/convince-project/active-plan>`_

To be filled by UoB.

simulate-plan
-------------
`convince-project/simulate-plan <https:///github.com/convince-project/simulate-plan>`_

To be filled by UoB.

scan
----
`convince-project/scan <https:///github.com/convince-project/scan>`_

To be filled by UniGe.

moon
----
`convince-project/moon <https:///github.com/convince-project/moon>`_

To be filled by UniGe.

mc-toolchain-jani
-----------------
`convince-project/mc-toolchain-jani <https:///github.com/convince-project/mc-toolchain-jani>`_

This is a toolbox for converting all specifications of components of a robotic system under investigation into a format which can be given as input to model checkers for verifying the robustness of the system functionalities. The resulting format used for model checking is `JANI <https://jani-spec.org>`_. 

The toolbox consist of a script to convert models describing the system and its environment together, given in the CONVINCE robotics JANI flavor as specified in the `data model repository <https://github.com/convince-project/data-model>`_, into `plain JANI <https://jani-spec.org>`_ accepted as input by model checkers. 
The second part of the toolbox centers around system specifications given in (SC)XML and how to convert them into a plain JANI file for model checking. This comprises property specification in temporal logic, currently given in JANI, a behavior tree in XML, ROS nodes and their pugins in SCXML, and an environment specification in SCXML.

model2code
----------
`convince-project/model2code <https:///github.com/convince-project/model2code>`_

This is a tool to generate skill level code starting from an SCXML model.
Starting from an SCXML model, XML file that describes the full model of the program, which includes the behavior tree, the skills and the components used in the system, and an XML file that describes the interfaces used between behavior tree and skills, and between skills and components, the program generates an header file and a source file that contains the code of the skill level.
The skills generated are based on a behavior tree structure and will have a ROS2 tick service in case they are a condition a ROS2 tick and halt services in case they are an action.


smc-storm
---------
`convince-project/smc_storm <https:///github.com/convince-project/smc_storm>`_

This is a statistical model checking engine for DTMC models given in JANI, which has been implemented as an extension to the famous `Storm model checker <https://stormchecker.org>`_. The tool and its documentation can be found in this `repository <https://github.com/convince-project/smc_storm>`_.


.. toctree::
   :hidden:

   tutorials
