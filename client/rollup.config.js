import babel from "@rollup/plugin-babel";
import commonjs from "@rollup/plugin-commonjs";
import resolve from "@rollup/plugin-node-resolve";
import replace from "@rollup/plugin-replace";
import typescript from "@rollup/plugin-typescript";
import url from "@rollup/plugin-url";
import path from "path";
import svelte from "rollup-plugin-svelte";
import { terser } from "rollup-plugin-terser";
import config from "sapper/config/rollup.js";
import sveltePreprocess from "svelte-preprocess";
import pkg from "./package.json";

const mode = process.env.NODE_ENV;
const dev = mode === "development";
const legacy = !!process.env.SAPPER_LEGACY_BUILD;

const replacements = {
  "process.env.default_num_gen_images": "5",
  "process.env.isExported": dev ? "false" : "true",
  "process.env.API_PATH": process.env.API_PATH
    ? `"${process.env.API_PATH}"`
    : `""`,
};

const onwarn = (warning, onwarn) =>
  (warning.code === "MISSING_EXPORT" && /'preload'/.test(warning.message)) ||
  (warning.code === "CIRCULAR_DEPENDENCY" &&
    /[/\\]@sapper[/\\]/.test(warning.message)) ||
  warning.code === "THIS_IS_UNDEFINED" ||
  onwarn(warning);

export default {
  client: {
    input: config.client.input().replace(/\.js$/, ".ts"),
    output: config.client.output(),
    plugins: [
      replace({
        "process.browser": true,
        "process.env.NODE_ENV": JSON.stringify(mode),
        ...replacements,
      }),
      svelte({
        dev,
        hydratable: true,
        preprocess: sveltePreprocess(),
        emitCss: true,
      }),
      url({
        sourceDir: path.resolve(__dirname, "src/node_modules/images"),
        publicPath: "/client/",
      }),
      resolve({
        browser: true,
        dedupe: ["svelte"],
        preferBuiltins: false,
      }),
      commonjs(),
      typescript({ sourceMap: dev, inlineSources: dev }),

      legacy &&
        babel({
          extensions: [".js", ".mjs", ".html", ".svelte"],
          babelHelpers: "runtime",
          exclude: ["node_modules/@babel/**"],
          presets: [
            [
              "@babel/preset-env",
              {
                targets: "> 0.25%, not dead",
              },
            ],
          ],
          plugins: [
            "@babel/plugin-syntax-dynamic-import",
            [
              "@babel/plugin-transform-runtime",
              {
                useESModules: true,
              },
            ],
          ],
        }),

      !dev &&
        terser({
          module: true,
        }),
    ],

    preserveEntrySignatures: false,
    onwarn,
  },

  server: {
    input: { server: config.server.input().server.replace(/\.js$/, ".ts") },
    output: config.server.output(),
    plugins: [
      replace({
        "process.browser": false,
        "process.env.NODE_ENV": JSON.stringify(mode),
        ...replacements,
      }),
      svelte({
        generate: "ssr",
        hydratable: true,
        preprocess: sveltePreprocess(),
        dev,
      }),
      url({
        sourceDir: path.resolve(__dirname, "src/node_modules/images"),
        publicPath: "/client/",
        emitFiles: false, // already emitted by client build
      }),
      resolve({
        dedupe: ["svelte"],
        preferBuiltins: false,
      }),
      commonjs(),
      typescript({ sourceMap: dev, inlineSources: dev }),
    ],
    external: Object.keys(pkg.dependencies).concat(
      require("module").builtinModules
    ),

    preserveEntrySignatures: "strict",
    onwarn,
  },

  serviceworker: {
    input: config.serviceworker.input().replace(/\.js$/, ".ts"),
    output: config.serviceworker.output(),
    plugins: [
      resolve({
        preferBuiltins: false,
      }),
      replace({
        "process.browser": true,
        "process.env.NODE_ENV": JSON.stringify(mode),
        ...replacements,
      }),
      commonjs(),
      typescript({ sourceMap: dev, inlineSources: dev }),
      !dev && terser(),
    ],

    preserveEntrySignatures: false,
    onwarn,
  },
};
