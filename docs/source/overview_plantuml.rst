Overview
========

.. uml::

    rectangle "Real System" as r {
        agent "Deliberation Layer" as rdelib
    }
    
    file "Model" as m {
        agent "Model of Deliberation Layer" as mdelib
    }

    agent "[[http://github.com/convince-project/refine-plan REFINE-PLAN]]" as refineplan

    rdelib -> refineplan
    refineplan -> mdelib
