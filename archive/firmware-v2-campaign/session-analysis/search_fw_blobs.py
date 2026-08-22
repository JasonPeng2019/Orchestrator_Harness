"""Search Firmware dangling blobs for old harness provider-adapter content."""
import subprocess

out = subprocess.run(
    ["git", "-C", "Firmware", "fsck", "--lost-found"],
    capture_output=True, text=True,
).stdout
blobs = [line.split()[-1] for line in out.splitlines() if "blob" in line]
print("total dangling blobs:", len(blobs))

targets = [
    b"ProviderLaunchSpec",
    b"register_provider_adapter",
    b"class QwenCodeProviderAdapter",
    b"notification_mode",
    b"workspace_overlay",
    b"def build_argv",
    b"orchestrator-worker-invocation/v1",
]

for b in blobs:
    data = subprocess.run(
        ["git", "-C", "Firmware", "cat-file", "-p", b],
        capture_output=True,
    ).stdout
    hits = [t.decode() for t in targets if t in data]
    if hits:
        print(b, len(data), hits)
