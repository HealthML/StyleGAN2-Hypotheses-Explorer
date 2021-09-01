# StyleGAN2 Hypotheses Explorer Client

## Setup

1. Install [NodeJS>=14.x](https://nodejs.org/en/).
2. Install the dependencies of this project via `npm install`.

## Run

1. Point the [API base path](src/api/api.ts) to an endpoint of the [StyleGAN2 Interactive Webclient API](docs/swagger.yml).
   1. This can be the bundled api server (The bundled api server can be started by following it's [README](../server/README.md#Run)).
2. Run the webclient with `npm run dev`.
3. Open `http://localhost:3000` in a webbrowser.

## Export

1. Export the webclient with `npm run export`.
2. The exported files can be found here: [`__sapper__/export`](__sapper__/export).
   1. If you export the client the API basepath is automatically set to the same host the webpage is served from.

### Export to Subdirectory

1. add the `--basepath <subdirectory>` flag to the `npm run export` command
2. uncomment the line annotated with `basepath for serving from subdirectory` in the [`server.ts`](src/server.ts) file
   - change the basepath to your subdirectory
