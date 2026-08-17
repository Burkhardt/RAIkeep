# RAIkeep terminal fonts

RAIkeep command-line help uses glyphs embedded in JetBrainsMono Nerd Font rather than Unicode symbols that depend on a platform fallback font. The recommended family is the no-ligatures proportional variant:

```text
JetBrainsMonoNL NFP
```

The Regular face has the PostScript name `JetBrainsMonoNLNFP-Regular` and is distributed by the official [Nerd Fonts project](https://github.com/ryanoasis/nerd-fonts).

RAIkeep does not redistribute the font binaries. The Blink stylesheet in this repository loads all four faces directly from the immutable official Nerd Fonts `v3.4.0` GitHub tag.

## Blink on iPadOS

1. Open Blink settings with `config` or `Command+,`.
2. Open **Appearance → Fonts → New Font**.
3. Use `JetBrainsMonoNL NFP` as the font name.
4. Paste this URL into **CSS FONT-FAMILY STYLESHEET**:

   ```text
   https://raw.githubusercontent.com/Burkhardt/RAIkeep/main/doc/JetBrainsMonoNLNerdFontPropo.css
   ```

5. Save the font, select it under Appearance, and open a new terminal session.

The stylesheet itself is [viewable on GitHub](https://github.com/Burkhardt/RAIkeep/blob/main/doc/JetBrainsMonoNLNerdFontPropo.css). Its font URLs point to `raw.githubusercontent.com/ryanoasis/nerd-fonts`; only the explanatory stylesheet is hosted by RAIkeep.

## macOS

Download the current official archive, extract the four family faces, and install them for the current user:

```bash
font_tmp="$(mktemp -d)"
curl -fL https://github.com/ryanoasis/nerd-fonts/releases/latest/download/JetBrainsMono.tar.xz \
  -o "$font_tmp/JetBrainsMono.tar.xz"
tar -xf "$font_tmp/JetBrainsMono.tar.xz" -C "$font_tmp" \
  JetBrainsMonoNLNerdFontPropo-Regular.ttf \
  JetBrainsMonoNLNerdFontPropo-Bold.ttf \
  JetBrainsMonoNLNerdFontPropo-Italic.ttf \
  JetBrainsMonoNLNerdFontPropo-BoldItalic.ttf
mkdir -p ~/Library/Fonts
cp "$font_tmp"/JetBrainsMonoNLNerdFontPropo-*.ttf ~/Library/Fonts/
```

Select `JetBrainsMonoNL NFP` in the terminal application's font settings. Apple Terminal reports the active face with:

```bash
osascript -e 'tell application "Terminal" to tell selected tab of front window to get {font name, font size}'
```

## Ubuntu and other fontconfig-based Linux systems

```bash
font_tmp="$(mktemp -d)"
curl -fL https://github.com/ryanoasis/nerd-fonts/releases/latest/download/JetBrainsMono.tar.xz \
  -o "$font_tmp/JetBrainsMono.tar.xz"
tar -xf "$font_tmp/JetBrainsMono.tar.xz" -C "$font_tmp" \
  JetBrainsMonoNLNerdFontPropo-Regular.ttf \
  JetBrainsMonoNLNerdFontPropo-Bold.ttf \
  JetBrainsMonoNLNerdFontPropo-Italic.ttf \
  JetBrainsMonoNLNerdFontPropo-BoldItalic.ttf
mkdir -p ~/.local/share/fonts/JetBrainsMonoNLNFP
cp "$font_tmp"/JetBrainsMonoNLNerdFontPropo-*.ttf ~/.local/share/fonts/JetBrainsMonoNLNFP/
fc-cache -f
fc-match "JetBrainsMonoNL NFP"
```

## Help-line rendering

The RAIkeep CLIs use boxed provider initials and boxed numeric options from Nerd Font's private-use glyph range. This avoids fallback-font substitution for the option glyphs. Help lines reserve two trailing cells so renderers such as Blink have room for the wider Propo advances without clipping visible text.

Font installation occurs on the rendering client. A CLI running on a remote Linux host through SSH cannot reliably determine which font Blink is using on an iPad, so RAIkeep documents and visually exercises the font instead of reporting an unreliable installation error.

For upstream installation alternatives and licensing, see the official [Nerd Fonts installation documentation](https://github.com/ryanoasis/nerd-fonts/blob/master/readme.md#font-installation).
