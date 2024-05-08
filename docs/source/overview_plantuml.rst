Overview
========

.. uml::

    skinparam agent {
        BackgroundColor White
        BorderColor Black
    }
    skinparam database {
        BackgroundColor White
        BorderColor Black
    }

    rectangle "Real System" as r {
        agent "Deliberation Layer" as rdelib
        agent "Skill Layer" as rskill
        agent "Functional Layer" as rfunc
        agent "Real Environment" as renv

        rdelib --> rskill
        rskill --> rfunc
        rfunc --> renv
    }

    file "Model" as m {
        agent "Deliberation Layer Model" as mdelib
        agent "Skill Layer Model" as mskill
        agent "Functional Layer Model" as mfunc
        agent "Environment Model" as menv

        mdelib --> mskill
        mskill --> mfunc
        mfunc --> menv
    }

    database "Knowledge Model\n" as k 

    ' renv -[hidden]> k
    ' k -[hidden]> menv

    ' WP2

    rectangle WP2 #line.dashed {
        agent sitaw [
        [[https:///github.com/convince-project/sit-aw SIT-AW]]\n
        ....
        CEA
        ]
    }

    ' sitaw -[hidden]> rskill
    rskill -> sitaw
    sitaw <-> k

    ' WP3

    rectangle WP3 #line.dashed {
        agent refineplan [
        [[https://github.com/convince-project/refine-plan REFINE-PLAN]]\n
        ....
        UoB
        ] 
        agent coverageplan [
        [[https:///github.com/convince-project/coverage-plan COVERAGE-PLAN]]\n
        ....
        UoB
        ]
        agent activeplan [
        [[https://github.com/convince-project/active-plan ACTIVE-PLAN]]\n
        ....
        UoB
        ] 
        agent simulateplan [
        [[https://github.com/convince-project/simulate-plan SIMULATE-PLAN]]\n
        ....
        UoB
        ] 
        ' refineplan -[hidden]-> coverageplan
        ' coverageplan -[hidden]-> activeplan
        ' activeplan -[hidden]-> simulateplan
    }

    coverageplan .. rfunc
    mdelib -> refineplan
    refineplan -> rdelib
    rdelib -> simulateplan
    k -> simulateplan
    k -> activeplan

    ' WP4

    rectangle WP4 #line.dashed {
        agent moon [
        [[https:///github.com/convince-project/moon MOON]]\n
        ....
        UniGe
        ]
        agent scan [
        [[https:///github.com/convince-project/scan SCAN]]\n
        ....
        UniGe
        ]
        agent jani [
        [[https:///github.com/convince-project/mc-toolchain-jaai MC-TOOLCHAIN-JAII]]\n
        ....
        Bosch
        ]
        agent storm [
        [[https:///github.com/convince-project/smc_storm SMC-STORM]]\n
        ....
        Bosch
        ]
        agent model2code [
        [[https:///github.com/convince-project/model2code MODEL2CODE]]\n
        ....
        IIT
        ]

        ' moon -[hidden]> scan
    }

    ' WP4 -[hidden]-> WP3

    scan <-> m
    moon <-> r
