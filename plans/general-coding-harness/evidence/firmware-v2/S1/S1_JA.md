# S1.JA test-author join

- Merge base / accepted production: `a0442b9419f66713e87be97f226e4afc6367e264`
- A1 commit merged first: `7ca3beb4e67fb98a7e02bfde4788c43c1fda354c`
- A1 merge commit: `3b6ae83`
- A2 commit merged second: `aa45ee9fb9edf581e89850018b233f56bd14b56d`
- Joined revision: `b534b5c17fc5e2aa476cacee88ff0f893243cf47`
- A1 plan SHA-256: `c96850ccd85062347532e7a5eda9e0003407aac2eb8c321a8c1b529ec7a1af41`
- A2 plan SHA-256: `2af4ebf9e913e1010f3505bdbc3c4c82dbb4c0db7625470e4aa6315f57ac4494`
- A2 draft dependency map SHA-256: `e7036f26bad62dd27d8b49057ca34fe3c8dbf989506afaaa48adb17e700429d5`

Ownership was disjoint: A1 added only `test_firmware_route_compatibility.py`; A2 added only `test_firmware_lifecycle_compatibility.py`. Both diffs passed `git diff --check`, and the ordered merges were conflict-free. No production or protected baseline test was changed by either author.

ROOT-IM rejected A2's dependency map as too narrow for the shared controller file and replaced it with `SHARED_CODE_DEPENDENCY_MAP.json`, conservatively identifying 19 protected baseline IDs across five directly dependent modules plus five new S1 IDs. This joined revision and map define S1.ST.
