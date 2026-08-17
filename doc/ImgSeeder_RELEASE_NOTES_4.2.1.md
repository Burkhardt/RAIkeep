# ImgSeeder 4.2.1

CLI-only maintenance release based on the published RAIkeep 4.2.0 libraries.

- Uses cloud-provider initials and numbered-option glyphs that are embedded in
  `JetBrainsMonoNLNerdFontPropo-Regular`, avoiding fallback-font width
  differences in help output.
- Corrects contextual option-description alignment.
- Reserves two terminal cells at the end of help lines to tolerate proportional
  Nerd Font metrics and renderers such as Blink.
- Reports `iorg v4.2.1` through the CLI version boundary.

Package dependencies remain `JsonPit 4.2.0`, `OsLibCore 4.2.0`,
`RaiUtils 4.2.0`, and `RaiImage 4.2.0`. No library package or umbrella version is
changed by this release.

Release verification: 16 ImgSeeder Release tests passed, and the package-only
build and package metadata were verified against the published 4.2.0
dependencies.
