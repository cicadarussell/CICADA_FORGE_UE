# POWERSHELL SWITCH FORWARDING FIX

## Problem

Phase 003I exposed this wrapper bug:

```text
Cannot process argument transformation on parameter 'OpenReport'.
Cannot convert value "System.String" to type "System.Management.Automation.SwitchParameter".
```

This happened because the master wrapper forwarded switches in a fragile way.

## Fix

Phase 003J uses an argument array and only adds switch names when switches are present.

Correct pattern:

```powershell
$CallArgs = @("-ExecutionPolicy", "Bypass", "-File", $ScriptPath)
if ($PassOpenReport) {
    $CallArgs += "-OpenReport"
}
& powershell @CallArgs
```

## Rule

Do not pass switch values as strings.

Either include the switch name or do not include it.
