# ImgSeeder 4.2.10 Release Notes

ImgSeeder 4.2.10 improves `iorg` root and tenant addressing.

- Adds `-a, --app` for an application root; iorg appends the conventional
  `Image` segment.
- Adds preferred `-t, --tenant`; `--subscriber` remains a compatibility alias.
- Retains `-r, --root` for an exact ImageTree root. Root and app are mutually
  exclusive, and app-root addressing requires an explicit tenant.
- Corrects the tenant help-row alignment and shows the unnamed-subscriber
  compatibility explanation only when that legacy form was actually used.
- Command synopses consistently show `[(-t|--tenant) <name>]` and
  `[(-p|--pathconv) <1|2|3|4>]` where applicable.

Regression coverage proves that `--app AIA --tenant nomsa` resolves the same
tree as the corresponding exact `--root AIA/Image/nomsa` form.
