# S1.CA accepted production revision

- Accepted production revision: `a0442b9419f66713e87be97f226e4afc6367e264`
- Product branch: `firmware/v2-s1-product`
- Exact base: `4699d27bd5bf7c0b41bbed9ddb6b0b7d019e215f`
- S1.P thread: `019fca2e-7484-73c2-bd59-bb791b7573db`
- Targeted R1 revival: `NO FINDINGS`, report SHA-256 `d42183182bcb6d43285977e987a7a8c4bd6198c26d2f948672ca40609c9ccb42`
- Targeted R2 revival: `NO FINDINGS`, report SHA-256 `5f849a367c9ba03eb942124e687ac92f4e000d8a4bbd0ad221b5bfd3782cd915`

The accepted production delta implements fail-closed mixed-route rejection for every real firmware-only and coding-only discriminator, including accepted coding aliases and coding-only nested fallback settings. Table tests are bound to the production constant sets. Retained valid coding and schema-less firmware routes remain unchanged. The lifecycle implementation outside this parser boundary did not change and retains its prior focused evidence.

The branch and worktree are clean at the recorded tip. This checkpoint admits the S1.A1/S1.A2 test-author fan-out; it does not yet close S1 or update the promoted candidate branch.
