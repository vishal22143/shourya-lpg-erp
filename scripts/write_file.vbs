Set fso = CreateObject("Scripting.FileSystemObject")
path = WScript.Arguments(0)
content = WScript.Arguments(1)
Set f = fso.CreateTextFile(path, True, True)
f.Write content
f.Close
