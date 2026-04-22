Tutorial: Generating ROS2 Skill Code with model2code
======================================================

This tutorial explains how to use the ``model2code`` tool to generate ROS2 skill code from an SCXML model file.

Overview
--------

``model2code`` is a tool that takes an ASCXML file describing a skill's state machine and generates a complete ROS2 package with C++ code, including Qt state machine integration.

Prerequisites
-------------

- The CONVINCE Docker environment is running.
- The ``model2code`` tool is installed (available in the Docker image).

Setup: Starting the Docker Environment
---------------------------------------

1. **Start the Docker container**:

   .. code-block:: bash

      docker compose run --rm base /bin/bash

   This opens an interactive bash shell inside the CONVINCE Docker environment.

2. **Navigate to the tutorials directory**:

   .. code-block:: bash

      cd /convince_ws/src/tutorials

   All commands in this tutorial should be run from this directory.

Steps
-----

1. **Prepare the input SCXML file**: Ensure your SCXML model is ready. For this tutorial, we'll use the ``PlaceObjectSkill.ascxml`` located at ``tutorials/roaml/skills/PlaceObjectSkill.ascxml``.

2. **Run the model2code command**:

   .. code-block:: bash

      model2code \
        --input_filename "/convince_ws/src/tutorials/roaml/skills/PlaceObjectSkill.ascxml" \
        --output_path "/convince_ws/src/tutorials/simulation/behavior_trees/generated_skill/place_object_skill" \
        --template_path "/model2code/template_skill"

   - ``--input_filename``: Path to the SCXML file describing the skill.
   - ``--output_path``: Directory where the generated ROS2 package will be created.
   - ``--template_path``: Path to the template directory containing the code templates.

3. **Build the generated package**:
   After generation, build the ROS2 package:

   .. code-block:: bash

      cd /convince_ws
      colcon build --packages-select place_object_skill

4. **Source the environment and run**:

   .. code-block:: bash

      source install/setup.bash
      ros2 run place_object_skill place_object_skill

Notes
-----

- The generated package includes C++ source files, CMakeLists.txt, package.xml, and Qt SCXML files.
- The skill implements ROS2 services for tick and halt operations.
- You can customize the generated code by modifying the templates in the ``template_skill`` directory.