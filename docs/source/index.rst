CONVINCE Toolchain Overview
===========================


Welcome to the CONVINCE toolchain documentation. 
The goal of the `CONVINCE project <https://convince-project.eu/>`_ is to provide an open source toolchain to improve robust robot deliberation with the help of planning, learning, and model checking techniques. 

This is the entry-point for the CONVINCE toolchain documentation. It provides an overview of all the individual components which are part of the large toolchain. Those components can be used standalone and also linked together as required for individual use cases.

.. .. uml::  overview.plantuml
..    :caption: CONVINCE Toolchain Overview
..    :alt: CONVINCE Toolchain Overview

.. image:: overview.png

The CONVINCE toolchain works as depicted above. The individual repos and documentations are linked from there.

In the following the CONVINCE toolchain components are briefly described. For more details please check out the individual repositories with their documentation and tutorial pages.


sit-aw
------
`convince-project/sit-aw <https:///github.com/convince-project/sit-aw>`_

SIT-AW is a software pipeline for robot situation awareness. It enables known and unknown anomaly detection, identification and resolution.

By the end of CONVINCE the pipeline will be made up of different software modules implementing approaches based on symbolic AI and deep learning. During robotic system operations, these modules will handle the detection and classification of unexpected situations (anomalies). Symbolic approaches rely on a knowledge base constituted by an ontology and its rules. Deep learning approaches rely on data collection, feature extraction and data fusion to be able to identify an anomaly as being known or unknown. The pipeline takes monitor alarms and sensory-data as inputs. Whenever an anomaly is classified as unknown, SIT-AW interacts with `ACTIVE-PLAN <https://convince-project.github.io/overview/#active-plan-simulate-plan>`_ to try to come up with an appropriate mitigation plan. This mitigation plan will be used in `SIT-L <https://convince-project.github.io/overview/#sit-l>`_ for learning new situations models.

For a list of available software modules in the current release of the SIT-AW pipeline refer to its `README <https://github.com/convince-project/sit-aw/tree/main?tab=readme-ov-file>`_ file.


sit-l
-----
SIT-L is a software module that implements techniques for the acquisition (learning) of new episodic and semantic memory from encountered unexpected situations that were not foreseen at design time (unknown anomalies). It closes the loop of robot situation awareness and increased robot autonomy. SIT-L is under development and will be release at a later stage of CONVINCE.

SIT-L represents the extraction of the new anomaly description, given the preprocessed sensory-data, monitor outputs, ontologies and from the found solution to resolve the anomaly, i.e., the output of `ACTIVE-PLAN/SIMULATE-PLAN <https://convince-project.github.io/overview/#active-plan-simulate-plan>`_. A new pair (anomaly description, mitigation strategy) is then added to the current knowledge base, which implies learning a new situation. Indeed, if the system encounters this situation again, it will be able to identify the anomaly as known and resolve it.


coverage-plan
-------------
| V1: `convince-project/coverage-plan <https:///github.com/convince-project/coverage-plan>`_
| V2: `convince-project/congestion-coverage-plan <TBC>`_

.. .. uml::

..    agent "\nSkill Layer\n" as rskill #LightYellow

..    agent coverageplan #PaleGreen [
..    [[https:///github.com/convince-project/coverage-plan COVERAGE-PLAN]]
..    ....
..    WP3 / UoB
..    ]

..    rskill . coverageplan

The CONVINCE toolbox contains two versions of COVERAGE-PLAN.

COVERAGE-PLAN V1
++++++++++++++++

COVERAGE-PLAN V1 is an online tool for *lifelong area coverage in dynamic and uncertain environments*.

COVERAGE-PLAN V1 operates on discrete grid environments. 
COVERAGE-PLAN V1 has two components: an online coverage planner, and a learned model of stochastic occupancy dynamics.
The dynamics model `captures the probability that a grid cell becomes occupied or free in the next timestep <https://ieeexplore.ieee.org/abstract/document/6385629>`_.
This model is learned over the robot's lifespan, where the model is updated after each coverage run using the robot's latest observations.
The online coverage planner uses the learned model to build and solve a `partially observable Markov decision process (POMDP) <https://www.sciencedirect.com/science/article/pii/S000437029800023X?via%3Dihub>`_ for area coverage.
The state-of-the-art `DESPOT <https://github.com/AdaCompNUS/despot>`_ algorithm is used to solve POMDPs.
Before deployment, the user must specify the map dimensions, the robot's starting position, the robot's field of view, and the time bound on coverage.

COVERAGE-PLAN V1 can be found `here <https://github.com/convince-project/coverage-plan>`__ and its documentation can be found `here <https://convince-project.github.io/coverage-plan>`__.
The documentation contains a tutorial demonstrating the coverage planner.

COVERAGE-PLAN V2
++++++++++++++++

COVERAGE-PLAN V2 is an online tool for *tour planning in crowded, human-populated environments*.

COVERAGE-PLAN V2 operates over a topological graph.
COVERAGE-PLAN V2 has two components: an online tour planner, and a learned model of human dynamics.
The dynamics model, known as a `CLiFF <https://ieeexplore.ieee.org/document/7835155/>`_ map, captures the speed and direction of human motion at different points in the environment.
This model is learned from human motion data collected on LIDARs placed around the environment.
The online tour planner uses the CLiFF map to build and solve an `MDP <https://onlinelibrary.wiley.com/doi/book/10.1002/9780470316887>`__.
The MDP is solved using `labeled real-time dynamic programming (LRTDP) <https://cdn.aaai.org/ICAPS/2003/ICAPS03-002.pdf>`_.
Before deployment, the user must specify the topological map and the robot's starting position.


COVERAGE-PLAN V2 can be found `here <TBC>`__ and its documentation can be found `here <TBC>`__.
The documentation contains a tutorial showing how to use the tour planner.


refine-plan
-----------
`convince-project/refine-plan <https:///github.com/convince-project/refine-plan>`_

REFINE-PLAN is an offline tool for *refining hand-designed behaviour trees (BTs)* to admit geometric reasoning and attain robustness under uncertainty, improving performance.


The input to REFINE-PLAN is a hand-designed BT.
REFINE-PLAN extracts a state space from the hand-designed BT, and learns the probabilistic dynamics of BT action nodes under different parameters.
These parameters describe the motion-level behaviour of action nodes.
To support model learning, we use an information-theoretic approach to efficiently collect data in simulation.
The simulation is provided by the user.
State space extraction is not implemented in the current release.
Given the extracted state space and a set of `Bayesian networks <http://mcb111.org/w06/KollerFriedman.pdf>`_ that describe robot dynamics, REFINE-PLAN constructs an `MDP <https://onlinelibrary.wiley.com/doi/book/10.1002/9780470316887>`__ and solves it using `Storm/Stormpy <https://moves-rwth.github.io/stormpy/>`_ to synthesise a policy.
This policy can then be converted back to a BT using `existing methods <https://ieeexplore.ieee.org/document/10105979>`_.


REFINE-PLAN can be found `here <https://github.com/convince-project/refine-plan>`__ and its documentation can be found `here <https://convince-project.github.io/refine-plan>`__.
The documentation contains a number of tutorials demonstrating the current functionality.


active/simulate-plan
-----------------------------
ACTIVE-PLAN and SIMULATE-PLAN are tools used for handling unknown anomalies.
These tools are currently being developed.
The input here is an anomalous state where the robot failed to perform an action, and the output is an anomaly-free state where the robot is now able to perform the action.
Anomalies are detected using `SIT-AW <https:///github.com/convince-project/sit-aw>`__.
`Explainable AI planning <https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=9635890>`__ is used to generate explanations about our systems, and these explanations will guide the robot to understand what went wrong and which actions need to be applied to reach an anomaly-free state.
`Failure Mode and Effects Analysis <https://iopscience.iop.org/article/10.1088/1757-899X/337/1/012033/pdf>`__ is used to store the unknown anomalies we have encountered, once we have recovered.
This is fed into a Bayesian Network to calculate the Conditional Probability Tables using `PyAgrum <https://pypi.org/project/pyAgrum/>`__ to infer which solution SIMULATE-PLAN can use to resolve the anomalies. 


scan
----
`convince-project/scan <https:///github.com/convince-project/scan>`_

SCAN (StatistiCal ANalyzer) is a statistical model checker developed
to verify large concurrent systems for which standard verification
techniques do not scale. The input model of SCAN is a combination of
Behavior Trees (BTs) described using behaviortree.cpp XML format, and
state machines (FSMs) described using SCXML (State Chart XML) format;
properties are described using an XML syntax for MTL (Metric Temporal
Logic) interpreted over discrete time traces. SCAN translates the
combination of BTs and FSMs into a Channel System (CS) whose
executions are sampled in order to find violations of the specified
properties or establish that such properties are verified 
with some probability and within some confidence interval. The
probability values and the size of the confidence intervals depend on
the amount of time given to SCAN to verify the system: allowing more
verification time will correspond to smaller confidence
intervals. Also, if the model is probabilistic, then the final result
of SCAN will depend on the probabilistic parameters of the model. In
other words, if the model is just non-deterministic, the probability of
satisfaction and corresponding confidence interval attached to a
specific property by SCAN will only depend on the computation time
allowed, whereas if probabilities are attached to transitions in the
model, this will also influence the final result emitted by SCAN. 


moon
----
`convince-project/moon <https:///github.com/convince-project/moon>`_

MOON (MOnitoring ONline) is a runtime monitor developed for CONVINCE
on top of the `ROSMonitoring tool <https://github.com/autonomy-and-verification-uol/ROSMonitoring>`_. MOON accepts the same description of
SCAN and provides monitor generation for properties and
models. Currently, only monitor generation for properties is
implemented on top of ROSMonitoring, working for ROS2 topics and
services. In perspective, the tool will include also monitoring for
models, i.e., the capability of ensuring that the concrete execution
of some elements of the control architecture or the environment
correspond to the abstract model utilized at design-time for
SCAN. MOON will notify violations of properties and models so that
other tools can be invoked to amend plans or models and adapt the
control architecture to new and unforeseen situations. 


as2fm
-----------------
`convince-project/as2fm <https:///github.com/convince-project/as2fm>`_

This is a toolbox for converting all specifications of components of a robotic system under investigation into a format which can be given as input to model checkers for verifying the robustness of the system functionalities. The resulting format used for model checking is `JANI <https://jani-spec.org>`_. 

The toolbox consist of a script to convert models describing the system and its environment together, given in the CONVINCE robotics JANI flavor as specified in the `data model repository <https://github.com/convince-project/data-model>`_, into `plain JANI <https://jani-spec.org>`_ accepted as input by model checkers. 
The second part of the toolbox centers around system specifications given in (SC)XML and how to convert them into a plain JANI file for model checking. This comprises property specification in temporal logic, currently given in JANI, a behavior tree in XML, ROS nodes and their plugins in SCXML, and an environment specification in SCXML.


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
