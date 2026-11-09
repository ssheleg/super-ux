# Agent test panel

<!-- Managed with super-ux (ux-contract v5). The agents an agent-tester walks
the agent-channel scenarios as (task-pipeline reads this file). Separate from
test-panel.md, the human panel, on purpose. Five agents, each with its grant,
its model class and the scenarios it walks. A grant here is a test-tenant
grant: the credential comes from the project's secret store, never this file. -->

## Panel

<!-- ### AG-01: Full-grant agent
- **Acts for:** P-01
- **Grant:** <every scope its principal holds>
- **Model class:** <the verification model the project uses>
- **Walks:** <SCN-… agent-channel scenarios>

### AG-02: Narrowly delegated agent
- **Acts for:** P-01
- **Grant:** <one scope, e.g. read-only billing>
- **Model class:** <…>
- **Walks:** <SCN-…: expects a typed refusal where its grant ends>

### AG-03: Automation with no conversation
- **Acts for:** <A-…, Kind: system>
- **Grant:** <the automation's own scope>
- **Model class:** none
- **Walks:** <SCN-… for CAP rows with an Automation trigger>

### AG-04: Cheap model
- **Acts for:** P-01
- **Grant:** <as AG-01>
- **Model class:** <a small, inexpensive model; advisory>
- **Walks:** <SCN-…: can the tool descriptions alone guide it>

### AG-05: Adversarial agent
- **Acts for:** P-01
- **Grant:** <as AG-02>
- **Model class:** <…>
- **Walks:** <SCN-… with injected content in what it reads; owed on a public surface>
-->
