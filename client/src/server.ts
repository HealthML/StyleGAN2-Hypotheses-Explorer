import * as sapper from "@sapper/server";
import compression from "compression";
import polka from "polka";
import sirv from "sirv";
const { PORT, NODE_ENV } = process.env;
const dev = NODE_ENV === "development";

polka()
  .use(
    // basepath for serving from subdirectory
    // "/StyleGAN2-Interactive-Webclient",
    compression({ threshold: 0 }) as any,
    sirv("static", { dev }),
    sapper.middleware()
  )
  .listen(PORT);
