import {
  defineConfig,
  presetAttributify,
  presetIcons,
  presetTypography,
  presetUno,
  presetWebFonts
} from 'unocss'

export default defineConfig({
  presets: [
    presetAttributify,
    presetIcons,
    presetTypography,
    presetUno,
    presetWebFonts(),
  ],
  cli: {
    entry: {
      patterns: ['src/wheke/frontend/templates/**/*.html'],
      outFile: 'src/wheke/frontend/static/css/styles.css',
    },
  },
})
