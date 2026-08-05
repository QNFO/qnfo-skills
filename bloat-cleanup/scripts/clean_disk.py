#!/usr/bin/env python3
"""Delete cache, temp, and bloatware files to free disk space."""
import os, shutil, sys

CLEANABLE_PATHS = [
    # System caches
    r"C:\Windows\Temp",
    r"C:\Windows\Prefetch",
    r"FILE:C:\hiberfil.sys",
    
    # Package caches
    "{local}\\npm-cache",
    "{local}\\pip",
    "{user}\\.npm",
    
    # Browser caches
    "{local}\\Google\\Chrome\\User Data\\Default\\Code Cache",
    "{local}\\Google\\Chrome\\User Data\\Default\\Service Worker",
    "{local}\\Google\\Chrome\\User Data\\GrShaderCache",
    "{local}\\Google\\Chrome\\User Data\\ShaderCache",
    "{local}\\Microsoft\\Edge\\User Data\\Default\\Code Cache",
    "{local}\\Microsoft\\Edge\\User Data\\ShaderCache",
    
    # VS Code caches
    "{roaming}\\Code\\CachedData",
    "{roaming}\\Code\\CachedExtensionVSIXs",
    "{roaming}\\Code\\Cache",
    
    # App caches
    "{local}\\D3DSCache",
    "{local}\\Microsoft\\Windows\\Explorer",
    "{local}\\Microsoft\\Office\\OTele",
    "{local}\\PC Manager Store",
    "{roaming}\\discord\\Cache",
    
    
    # Crash dumps
    r"C:\Windows\Minidump",
    r"FILE:C:\Windows\MEMORY.DMP",
    "{local}\\CrashDumps",
    
    # Temp
    "{local}\\Temp",
]

def clean_path(path):
    """Delete a path (file or directory). Returns (success, size_freed)."""
    if not os.path.exists(path):
        return "SKIP", 0
    
    # Get size before deletion
    try:
        if os.path.isfile(path):
            sz = os.path.getsize(path)
        else:
            sz = sum(os.path.getsize(os.path.join(r,f)) for r,_,fs in os.walk(path) 
                    for f in fs if os.path.isfile(os.path.join(r,f)))
    except:
        sz = 0
    
    try:
        if os.path.isfile(path):
            os.remove(path)
        else:
            shutil.rmtree(path, ignore_errors=True)
        return "DONE", sz
    except PermissionError:
        return "ACCESS DENIED (needs admin)", sz
    except Exception as e:
        return f"ERROR: {e}", sz

def main():
    user = os.environ["USERPROFILE"]
    local = os.environ.get("LOCALAPPDATA", os.path.join(user, "AppData", "Local"))
    roaming = os.path.join(user, "AppData", "Roaming")
    
    total_freed = 0
    total_count = 0
    
    for path_template in CLEANABLE_PATHS:
        # Handle FILE: prefix for single files
        is_file = path_template.startswith("FILE:")
        if is_file:
            path_template = path_template[5:]
        
        # Expand variables
        path = path_template.format(user=user, local=local, roaming=roaming)
        
        if not os.path.exists(path):
            continue
        
        label = os.path.basename(path)
        if len(path) > 65:
            label = "..." + path[-62:]
        
        status, sz = clean_path(path)
        total_freed += sz
        total_count += 1
        
        if sz > 0 or status != "SKIP":
            print(f"  [{status}] {label}: {sz/1048576:.1f} MB")
    
    print(f"\nFreed {total_freed/1048576:.1f} MB ({total_freed/1073741824:.2f} GB) from {total_count} locations")
    return total_freed

if __name__ == "__main__":
    main()
