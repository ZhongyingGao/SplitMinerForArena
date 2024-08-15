Set myarena = CreateObject("arena.application")
myarena.Visible = True
Set Model = myarena.Models.Add()
 Set CreateBasic = Model.Modules.Create("BasicProcess", "Create", 1250, 700)
 Debug.Print CreateBasic.shape.Tag
 CreateBasic.shape.Tag = "gxg55"
  Debug.Print CreateBasic.shape.Tag