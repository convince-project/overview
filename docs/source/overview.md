# Overview

```{mermaid}
flowchart TB
  m ~~~ r

  mdelib ~~~ rdelib
  mskill ~~~ rskill
  mfunc ~~~ rfunc
  menv ~~~ renv

  subgraph r[Real System]
    rdelib[Deliberation Layer] --> rskill[Skill Layer]
    rskill --> rfunc[Functional Layer]
    rfunc --> renv[Real Environment]
  end

  subgraph m[System Model]
    mdelib[Deliberation Model] --> mskill[Skill Models]
    mskill --> mfunc[Functional Models]
    mfunc --> menv[Environment Model]
  end

  rdelib -- copy --> mdelib

  rskill --> mc-toolchain-jani[<a href="http://github.com/convince-project/mc-toolchain-jani">mc-toolchain-jani<a/>] 
   --> mskill
  rdelib --> mc-toolchain-jani
  rfunc --> mc-toolchain-jani
  mc-toolchain-jani

  m --> moon[<a href="http://github.com/convince-project/moon">moon<a/>] 
   --> m

  mdelib --> REFINE-PLAN[<a href="http://github.com/convince-project/refine-plan">REFINE-PLAN<a/>] 
  REFINE-PLAN --> rdelib

  mc-toolchain-jani ~~~ REFINE-PLAN
  

```
<!-- There is a bug in mermaid that causes issues here https://github.com/mermaid-js/mermaid/issues/2509 -->