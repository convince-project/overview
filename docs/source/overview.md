# Overview

```{mermaid}
flowchart LR
  subgraph Real System
    direction TB
    rdelib[Deliberation Layer] --> rskill[Skill Layer]
    rskill --> rfunc[Functional Layer]
    rfunc --> renv[Real Environment]
  end

  rdelib --> mdelib

  subgraph System Model
    direction TB
    mdelib[Deliberation Model] --> mskill[Skill Models]
    mskill --> mfunc[Functional Models]
    mfunc --> menv[Environment Model]
  end

  mdelib --> REFINE-PLAN[<a href="http://github.com/convince-project/refine-plan">REFINE-PLAN<a/>] 
  REFINE-PLAN --> rskill

```
