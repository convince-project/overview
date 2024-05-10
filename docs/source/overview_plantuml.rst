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
        agent "\nDeliberation Layer\n" as rdelib #LightYellow
        agent "\nSkill Layer\n" as rskill #LightYellow
        agent "\nFunctional Layer\n" as rfunc #LightYellow
        agent "\nReal Environment\n" as renv #LightYellow

        rdelib --> rskill
        rskill --> rfunc
        rfunc --> renv
    }

    file "Model" as m {
        agent "\nDeliberation Layer Model\n" as mdelib #LightBlue
        agent "\nSkill Layer Model\n" as mskill #LightBlue
        agent "\nFunctional Layer Model\n" as mfunc #LightBlue
        agent "\nEnvironment Model\n" as menv #LightBlue

        mdelib --> mskill
        mskill --> mfunc
        mfunc --> menv
    }

    renv -[hidden]> menv
    rdelib -[hidden]> mdelib

    database "Knowledge Model\n" as k 

    ' renv -[hidden]> k
    ' k -[hidden]> menv

    ' WP2

    ' rectangle WP2 #line.dashed{
    agent sitaw #LightGreen [
    [[https:///github.com/convince-project/sit-aw SIT-AW]]
    ....
    WP2 / CEA
    ]
    ' }

    ' sitaw -[hidden]> rskill
    rskill -> sitaw
    sitaw <-> k

    ' WP3

    ' rectangle WP3 #line.dashed {
    agent refineplan #PaleGreen [
    [[https://github.com/convince-project/refine-plan REFINE-PLAN]]
    ....
    WP3 / UoB
    ] 
    agent coverageplan #PaleGreen [
    [[https:///github.com/convince-project/coverage-plan COVERAGE-PLAN]]
    ....
    WP3 / UoB
    ]
    agent activeplan #PaleGreen [
    [[https://github.com/convince-project/active-plan ACTIVE-PLAN]]
    ....
    WP3 / UoB
    ] 
    agent simulateplan #PaleGreen [
    [[https://github.com/convince-project/simulate-plan SIMULATE-PLAN]]
    ....
    WP3 / UoB
    ] 
    refineplan -[hidden]-> simulateplan
    simulateplan -[hidden]-> activeplan
    ' }

    coverageplan .. rfunc
    mdelib -> refineplan
    refineplan -> rdelib
    rdelib -> simulateplan
    k -> simulateplan
    k -> activeplan

    ' WP4

    ' rectangle WP4 #line.dashed {
    agent moon #TECHNOLOGY [
    [[https:///github.com/convince-project/moon MOON]]
    ....
    WP4 / UniGe
    ]
    together {
        agent scan #TECHNOLOGY [
        [[https:///github.com/convince-project/scan SCAN]]
        ....
        WP4 / UniGe
        ]
        agent storm #TECHNOLOGY [
        [[https:///github.com/convince-project/smc_storm SMC-STORM]]
        ....
        WP4 / Bosch
        ]
        scan -[hidden]-> storm
    }
    together {
        agent jani #TECHNOLOGY [
        [[https:///github.com/convince-project/mc-toolchain-jaai MC-TOOLCHAIN-JAII]]
        ....
        WP4 / Bosch
        ]
        agent model2code #TECHNOLOGY [
        [[https:///github.com/convince-project/model2code MODEL2CODE]]
        ....
        WP4 / IIT
        ]
    }
    activeplan -[hidden]-> jani
    activeplan -[hidden]-> model2code

    ' moon -[hidden]> scan
    moon -[hidden]-> rdelib

    moon <-> r

    m -> storm
    m -> scan

    rfunc -> jani
    jani -> mfunc
    rfunc <- model2code
    model2code <- mfunc