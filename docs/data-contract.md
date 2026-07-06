# Data Contract

## CAD IR

Required top-level fields:

```json
{
  "project_id": "",
  "global_units": "mm",
  "inputs": [],
  "coordinate_system": {},
  "constraints": [],
  "parts": [],
  "assemblies": [],
  "catalog_requirements": [],
  "uncertainties": [],
  "source_trace": []
}
```

Rules:

- `project_id` must be stable for the project.
- Units are millimeters by default.
- Unknown values belong in `uncertainties`.
- Every explicit constraint should have a source reference.

## Component Catalog

Required CSV fields:

```text
component_id,category,name,confidence,catalog_status,source,bbox_x_mm,bbox_y_mm,bbox_z_mm,notes
```

Allowed confidence values:

- `high`
- `medium`
- `low`
- `needs_review`

## Placement Plan

Required CSV fields:

```text
placement_id,component_id,parent_assembly,tx_mm,ty_mm,tz_mm,rx_deg,ry_deg,rz_deg,datum_rule,status,notes
```

Status guidance:

- `candidate`: safe for draft planning.
- `manual_review`: must be reviewed before final downstream build.
- `approved`: explicitly approved for downstream build.
- `blocked`: missing source data or invalid placement.

## Execution Graph

Each node should contain:

```json
{
  "node_id": "",
  "node_type": "",
  "inputs": [],
  "outputs": [],
  "depends_on": [],
  "status": "pending",
  "checkpoint_path": "",
  "trace": []
}
```
