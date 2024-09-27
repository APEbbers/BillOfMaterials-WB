![BillOfMaterialsWB](https://github.com/user-attachments/assets/ef66fa69-b78e-4210-afe2-a1476f601fa0)

# Bill of Materials-WB

A workbench to create Bill of Materials (BoM) independent of the assembly workbench of your choice.
With this workbench, different types of the BoM can be created:
* a total BoM with all the parts and subassemblies (the deepest level can be set).
* a summary BoM.
* a parts only BoM.
* a first level BoM (useful for assembly pages.
* a raw BoM. (This is a BoM, just as is. No summation of parts and assemblies. Can be used for testing or creating your own BoM in programs like Excel.)\
* Patterns are supported for Assembly 4.
Standard the following columns are added to the (BoM):
* Number.
* Quantity.
* Label. -> This will be the label of the original part or assembly.\
  For example in an assembly 3 assembly, parts are named like "Link001". This will be replaced with their original label like "bearing", "axis", etc).
* Description -> This is label2 in the property view.

Optionally, every property from the property view can be added from either the assembly document or a document selected in the tree.  

## Supported assembly types:
* a2plus
* Assembly 3
* Assembly 4
* Internal assembly workbench (This workbench is still in development)
* Applink / ApplinkGroup assemblies
* AppPart assemblies
* Multi body parts

## License:
LGPL2.+
