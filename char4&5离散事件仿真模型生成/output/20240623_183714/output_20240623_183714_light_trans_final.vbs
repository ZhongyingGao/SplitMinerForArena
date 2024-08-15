set app = createobject("arena.application")
app.visible=true
set Model=app.models.add()
Set Process = Model.Modules.Create("BasicProcess", "Create", 1400, 700)
Process.Data("Units") = "Minutes"
Process.Data("Value") = "8"
Set Process = Model.Modules.Create("BasicProcess", "Resource", 0, 0)
Process.Data("Name") = "Resource 1"
Set Process = Model.Modules.Create("BasicProcess", "Process", 2100, 700)
Process.Data("Name") = "Mould"
Process.Data("Units") = "Seconds"
Process.Data("Action") = "Seize Delay Release"
Process.Data("DelayType") = "Expression"
Process.Data("Resource Type(1)") = "Resource"
Process.Data("Resource Name(1)") = "Resource 1"
Process.Data("Expression") = "UNIF(220.0,265.0)"
Process.Shape.Selected = True
Set Process = Model.Modules.Create("BasicProcess", "Resource", 0, 0)
Process.Data("Name") = "Resource 2"
Set Process = Model.Modules.Create("BasicProcess", "Process", 2800, 700)
Process.Data("Name") = "Assemble"
Process.Data("Units") = "Seconds"
Process.Data("Action") = "Seize Delay Release"
Process.Data("DelayType") = "Expression"
Process.Data("Resource Type(1)") = "Resource"
Process.Data("Resource Name(1)") = "Resource 2"
Process.Data("Expression") = "UNIF(291.0,321.0)"
Process.Shape.Selected = True
Set Process = Model.Modules.Create("BasicProcess", "Resource", 0, 0)
Process.Data("Name") = "Resource 3"
Set Process = Model.Modules.Create("BasicProcess", "Process", 3500, 700)
Process.Data("Name") = "Blend"
Process.Data("Units") = "Seconds"
Process.Data("Action") = "Seize Delay Release"
Process.Data("DelayType") = "Expression"
Process.Data("Resource Type(1)") = "Resource"
Process.Data("Resource Name(1)") = "Resource 3"
Process.Data("Expression") = "UNIF(339.0,362.0)"
Process.Shape.Selected = True
Set Process = Model.Modules.Create("BasicProcess", "Resource", 0, 0)
Process.Data("Name") = "Resource 4"
Set Process = Model.Modules.Create("BasicProcess", "Process", 1400, 1400)
Process.Data("Name") = "Debubble"
Process.Data("Units") = "Seconds"
Process.Data("Action") = "Seize Delay Release"
Process.Data("DelayType") = "Expression"
Process.Data("Resource Type(1)") = "Resource"
Process.Data("Resource Name(1)") = "Resource 4"
Process.Data("Expression") = "UNIF(266.0,285.0)"
Process.Shape.Selected = True
Set Process = Model.Modules.Create("BasicProcess", "Resource", 0, 0)
Process.Data("Name") = "Resource 5"
Set Process = Model.Modules.Create("BasicProcess", "Process", 2100, 1400)
Process.Data("Name") = "Grout"
Process.Data("Units") = "Seconds"
Process.Data("Action") = "Seize Delay Release"
Process.Data("DelayType") = "Expression"
Process.Data("Resource Type(1)") = "Resource"
Process.Data("Resource Name(1)") = "Resource 5"
Process.Data("Expression") = "UNIF(899.0,930.0000000000001)"
Process.Shape.Selected = True
Set Process = Model.Modules.Create("BasicProcess", "Resource", 0, 0)
Process.Data("Name") = "Resource 6"
Set Process = Model.Modules.Create("BasicProcess", "Process", 2800, 1400)
Process.Data("Name") = "Fitting"
Process.Data("Units") = "Seconds"
Process.Data("Action") = "Seize Delay Release"
Process.Data("DelayType") = "Expression"
Process.Data("Resource Type(1)") = "Resource"
Process.Data("Resource Name(1)") = "Resource 6"
Process.Data("Expression") = "UNIF(544.0,561.0)"
Process.Shape.Selected = True
Set Process = Model.Modules.Create("BasicProcess", "Resource", 0, 0)
Process.Data("Name") = "Resource 7"
Set Process = Model.Modules.Create("BasicProcess", "Process", 3500, 1400)
Process.Data("Name") = "Pouring"
Process.Data("Units") = "Seconds"
Process.Data("Action") = "Seize Delay Release"
Process.Data("DelayType") = "Expression"
Process.Data("Resource Type(1)") = "Resource"
Process.Data("Resource Name(1)") = "Resource 7"
Process.Data("Expression") = "UNIF(123.0,136.0)"
Process.Shape.Selected = True
Set Process = Model.Modules.Create("BasicProcess", "Resource", 0, 0)
Process.Data("Name") = "Resource 8"
Set Process = Model.Modules.Create("BasicProcess", "Process", 1400, 2100)
Process.Data("Name") = "Clean"
Process.Data("Units") = "Seconds"
Process.Data("Action") = "Seize Delay Release"
Process.Data("DelayType") = "Expression"
Process.Data("Resource Type(1)") = "Resource"
Process.Data("Resource Name(1)") = "Resource 8"
Process.Data("Expression") = "UNIF(351.0,382.0)"
Process.Shape.Selected = True
Set Process = Model.Modules.Create("BasicProcess", "Resource", 0, 0)
Process.Data("Name") = "Resource 9"
Set Process = Model.Modules.Create("BasicProcess", "Process", 2100, 2100)
Process.Data("Name") = "Cut"
Process.Data("Units") = "Seconds"
Process.Data("Action") = "Seize Delay Release"
Process.Data("DelayType") = "Expression"
Process.Data("Resource Type(1)") = "Resource"
Process.Data("Resource Name(1)") = "Resource 9"
Process.Data("Expression") = "UNIF(208.0,224.0)"
Process.Shape.Selected = True
Set Process = Model.Modules.Create("BasicProcess", "Resource", 0, 0)
Process.Data("Name") = "Resource 10"
Set Process = Model.Modules.Create("BasicProcess", "Process", 2800, 2100)
Process.Data("Name") = "Polish"
Process.Data("Units") = "Seconds"
Process.Data("Action") = "Seize Delay Release"
Process.Data("DelayType") = "Expression"
Process.Data("Resource Type(1)") = "Resource"
Process.Data("Resource Name(1)") = "Resource 10"
Process.Data("Expression") = "UNIF(182.0,206.0)"
Process.Shape.Selected = True
Model.Modules.Create "BasicProcess", "Dispose", 3500, 2100
Model.ReplicationLength = 32
Model.DisableRandomness = "False"
Model.SaveAs "D:\BPMN2Arena\output\20240623_183714\Model1.doe"
Model.BatchMode = True
Model.DisableRandomness = "False"
Model.DisplayDefaultReport = smAlwaysDisplay
Model.DefaultReport = "SIMAN Summary Report(.out file)"
Model.DisableReportDatabase = True
Model.GO
Model.Save
app.quit
