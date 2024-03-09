<img src="https://github.com/APEbbers/BillOfMaterials-WB/assets/10145631/bda087ef-d360-4278-a071-93f42ee5612b" height=150px width=150px>

# Bill of Materials-WB

A workbench to create Bill of Materials (BoM) independent of the assembly workbench of your choice.
With this workbench, different types of the BoM can be created:
- a total BoM with all the parts and subassemblies (the deepest level can be set).
- a summary BoM.
- a parts only BoM.
- a first level BoM (useful for assembly pages.
- a raw BoM. (This is a BoM, just as is. No summation of parts and assemblies. Can be used for testing or creating your own BoM in programs like Excel.)\
Standard the following columns are added to the (BoM):
- Number.
- Quantity.
- Label. -> This will be the label of the original part or assembly.
  For example in an assembly 3 assembly, parts are named like "Link001". This will be replaced with their original label like "bearing", "axis", etc).
- Description -> This is label2 in the property view.

Optionally, every property from the property view can be added from either the assembly document or a document selected in the tree.
For debugging the option "Enable extra columns for debug" can be enabled. This option will add the following columns:
- Original label. -> The original name in the assembly. For example in an assembly 3 assembly this will be "Link001", "Link002", etc.
- Type. -> Part or Assembly
- Internal name.
- Fullname.
- TypeId.
<br/>

## Supported assembly types:
- a2plus
- Assembly 3
- Assembly 4
- Internal assembly workbench (This workbench is still in development)
- Applink / ApplinkGroup assemblies
- AppPart assemblies
<br/>

This workbench is still under development. Therefore there are some limitations.<br/>
Support for the following assemblies, workbenches and futures are planned:
- Improvement on assembly type detection, so assemblies can be placed in groups. -> Done. Ready for testing
- Support for the Arch WB
- Support for multi-body parts (Part WB)
- One function to support a mixed structure of all assembly workbenches
- A function to add the BoM to a TechDraw page template
- Mass calculation based on shape and material
- outer dimensions of items

## License:
LGPL2.+
