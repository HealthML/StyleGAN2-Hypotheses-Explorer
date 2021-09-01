// @ts-nocheck
/// <reference path="./custom.d.ts" />
// tslint:disable
/**
 * StyleGAN2 Interactive Webclient API
 * No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)
 *
 * OpenAPI spec version: 2.0.0
 *
 *
 * NOTE: This file is auto generated by the swagger code generator program.
 * https://github.com/swagger-api/swagger-codegen.git
 * Do not edit the file manually.
 */

import * as url from "url";
import type { Configuration } from "./configuration";
const isomorphicFetch = process.browser ? fetch : undefined;

const BASE_PATH = () =>
  (process.env.isExported
    ? location.origin + location.pathname + "/api/v2"
    : process.env.API_PATH
    ? process.env.API_PATH
    : `http://${location.hostname}:8080/api/v2`
  ).replace(/\/+$/, "");

/**
 *
 * @export
 */
export const COLLECTION_FORMATS = {
  csv: ",",
  ssv: " ",
  tsv: "\t",
  pipes: "|",
};

/**
 *
 * @export
 * @interface FetchAPI
 */
export interface FetchAPI {
  (url: string, init?: any): Promise<Response>;
}

/**
 *
 * @export
 * @interface FetchArgs
 */
export interface FetchArgs {
  url: string;
  options: any;
}

/**
 *
 * @export
 * @class BaseAPI
 */
export class BaseAPI {
  protected configuration: Configuration;

  constructor(
    configuration?: Configuration,
    protected basePath: string = BASE_PATH(),
    protected fetch: FetchAPI = isomorphicFetch
  ) {
    if (configuration) {
      this.configuration = configuration;
      this.basePath = configuration.basePath || this.basePath;
    }
  }
}

/**
 *
 * @export
 * @class RequiredError
 * @extends {Error}
 */
export class RequiredError extends Error {
  name: "RequiredError";
  constructor(public field: string, msg?: string) {
    super(msg);
  }
}

/**
 *
 * @export
 * @interface EvaluateImagesBatch
 */
export interface EvaluateImagesBatch {
  /**
   *
   * @type {number}
   * @memberof EvaluateImagesBatch
   */
  generatorId: number;
  /**
   *
   * @type {Array<StyleConfiguration>}
   * @memberof EvaluateImagesBatch
   */
  styles: Array<StyleConfiguration>;
}
/**
 *
 * @export
 * @interface Evaluator
 */
export interface Evaluator extends Model {}
/**
 *
 * @export
 * @interface Generator
 */
export interface Generator extends Model {
  /**
   * The number of layers of this model. (not affected by reduceNumberOfLayersBy)
   * @type {number}
   * @memberof Generator
   */
  numberOfLayers: number;
  /**
   *
   * @type {GeneratorSettings}
   * @memberof Generator
   */
  settings: GeneratorSettings;
  /**
   * All styles have to be rounded to this step size.
   * @type {number}
   * @memberof Generator
   */
  stepSize: number;
  /**
   * Use only get functions if this is true.
   * @type {boolean}
   * @memberof Generator
   */
  offlineMode: boolean;
}
/**
 *
 * @export
 * @interface GeneratorSettings
 */
export interface GeneratorSettings {
  /**
   * Number of styles per layer
   * @type {number}
   * @memberof GeneratorSettings
   */
  numGenStylesPerLayer: number;
  /**
   * If true the style images per layer will look the same
   * @type {boolean}
   * @memberof GeneratorSettings
   */
  useSameStylesForAllLayers: boolean;
  /**
   * Reducing the number of layers groups together layers in the view. e.g. if 2 layers are reduced the first and second displayed layer will actually be the first and second, and the third and fourth layers.
   * @type {number}
   * @memberof GeneratorSettings
   */
  reduceNumberOfLayersBy: number;
  /**
   * If present the generated styles will create images similar to these images. The images are stored in base64 encoding.
   * @type {Array<string>}
   * @memberof GeneratorSettings
   */
  stylesFromImages?: Array<string>;
  /**
   * If existent the generated styles will be optimized to one end of the evaluator ratings of the evaluation model with this id.
   * @type {number}
   * @memberof GeneratorSettings
   */
  optimizeStyles?: number;
}
/**
 *
 * @export
 * @interface Model
 */
export interface Model {
  /**
   * Unique id of this model
   * @type {number}
   * @memberof Model
   */
  id: number;
  /**
   * Human readable name of the model
   * @type {string}
   * @memberof Model
   */
  name: string;
}
/**
 *
 * @export
 * @interface ModelsArray
 */
export interface ModelsArray {
  /**
   *
   * @type {Array<Generator>}
   * @memberof ModelsArray
   */
  generators: Array<Generator>;
  /**
   *
   * @type {Array<Evaluator>}
   * @memberof ModelsArray
   */
  evaluators: Array<Evaluator>;
}
/**
 *
 * @export
 * @interface Style
 */
export interface Style {
  /**
   *
   * @type {number}
   * @memberof Style
   */
  generatorId: number;
  /**
   *
   * @type {StyleConfiguration}
   * @memberof Style
   */
  style: StyleConfiguration;
}
/**
 * Only one of styleArray and singleStyle may be present
 * @export
 * @interface StyleConfiguration
 */
export interface StyleConfiguration {
  /**
   *
   * @type {Array<StyleConfigurationStyleArray>}
   * @memberof StyleConfiguration
   */
  styleArray?: Array<StyleConfigurationStyleArray>;
  /**
   *
   * @type {StyleConfigurationSingleStyle}
   * @memberof StyleConfiguration
   */
  singleStyle?: StyleConfigurationSingleStyle;
}
/**
 *
 * @export
 * @interface StyleConfigurationSingleStyle
 */
export interface StyleConfigurationSingleStyle {
  /**
   *
   * @type {number}
   * @memberof StyleConfigurationSingleStyle
   */
  layer: number;
  /**
   *
   * @type {number}
   * @memberof StyleConfigurationSingleStyle
   */
  id: number;
}
/**
 *
 * @export
 * @interface StyleConfigurationStyleArray
 */
export interface StyleConfigurationStyleArray {
  /**
   *
   * @type {number}
   * @memberof StyleConfigurationStyleArray
   */
  style1: number;
  /**
   *
   * @type {number}
   * @memberof StyleConfigurationStyleArray
   */
  style2?: number;
  /**
   *
   * @type {number}
   * @memberof StyleConfigurationStyleArray
   */
  proportionStyle1?: number;
}
/**
 * EvaluatorApi - fetch parameter creator
 * @export
 */
export const EvaluatorApiFetchParamCreator = function (
  configuration?: Configuration
) {
  return {
    /**
     *
     * @summary Evaluate images from mixed styles and return them in order
     * @param {EvaluateImagesBatch} body
     * @param {number} evaluatorId
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     */
    evaluatorEvaluatorIdEvaluatePost(
      body: EvaluateImagesBatch,
      evaluatorId: number,
      options: any = {}
    ): FetchArgs {
      // verify required parameter 'body' is not null or undefined
      if (body === null || body === undefined) {
        throw new RequiredError(
          "body",
          "Required parameter body was null or undefined when calling evaluatorEvaluatorIdEvaluatePost."
        );
      }
      // verify required parameter 'evaluatorId' is not null or undefined
      if (evaluatorId === null || evaluatorId === undefined) {
        throw new RequiredError(
          "evaluatorId",
          "Required parameter evaluatorId was null or undefined when calling evaluatorEvaluatorIdEvaluatePost."
        );
      }
      const localVarPath = `/evaluator/{evaluatorId}/evaluate`.replace(
        `{${"evaluatorId"}}`,
        encodeURIComponent(String(evaluatorId))
      );
      const localVarUrlObj = url.parse(localVarPath, true);
      const localVarRequestOptions = Object.assign({ method: "POST" }, options);
      const localVarHeaderParameter = {} as any;
      const localVarQueryParameter = {} as any;

      localVarHeaderParameter["Content-Type"] = "application/json";

      localVarUrlObj.query = Object.assign(
        {},
        localVarUrlObj.query,
        localVarQueryParameter,
        options.query
      );
      // fix override query string Detail: https://stackoverflow.com/a/7517673/1077943
      delete localVarUrlObj.search;
      localVarRequestOptions.headers = Object.assign(
        {},
        localVarHeaderParameter,
        options.headers
      );
      const needsSerialization =
        <any>"EvaluateImagesBatch" !== "string" ||
        localVarRequestOptions.headers["Content-Type"] === "application/json";
      localVarRequestOptions.body = needsSerialization
        ? JSON.stringify(body || {})
        : body || "";

      return {
        url: url.format(localVarUrlObj),
        options: localVarRequestOptions,
      };
    },
    /**
     *
     * @summary Get the rating of a generated image
     * @param {number} evaluatorId
     * @param {string} style
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     */
    evaluatorEvaluatorIdEvaluateStyleGet(
      evaluatorId: number,
      style: string,
      options: any = {}
    ): FetchArgs {
      // verify required parameter 'evaluatorId' is not null or undefined
      if (evaluatorId === null || evaluatorId === undefined) {
        throw new RequiredError(
          "evaluatorId",
          "Required parameter evaluatorId was null or undefined when calling evaluatorEvaluatorIdEvaluateStyleGet."
        );
      }
      // verify required parameter 'style' is not null or undefined
      if (style === null || style === undefined) {
        throw new RequiredError(
          "style",
          "Required parameter style was null or undefined when calling evaluatorEvaluatorIdEvaluateStyleGet."
        );
      }
      const localVarPath = `/evaluator/{evaluatorId}/evaluate/{style}`
        .replace(`{${"evaluatorId"}}`, encodeURIComponent(String(evaluatorId)))
        .replace(`{${"style"}}`, encodeURIComponent(String(style)));
      const localVarUrlObj = url.parse(localVarPath, true);
      const localVarRequestOptions = Object.assign({ method: "GET" }, options);
      const localVarHeaderParameter = {} as any;
      const localVarQueryParameter = {} as any;

      localVarUrlObj.query = Object.assign(
        {},
        localVarUrlObj.query,
        localVarQueryParameter,
        options.query
      );
      // fix override query string Detail: https://stackoverflow.com/a/7517673/1077943
      delete localVarUrlObj.search;
      localVarRequestOptions.headers = Object.assign(
        {},
        localVarHeaderParameter,
        options.headers
      );

      return {
        url: url.format(localVarUrlObj),
        options: localVarRequestOptions,
      };
    },
  };
};

/**
 * EvaluatorApi - functional programming interface
 * @export
 */
export const EvaluatorApiFp = function (configuration?: Configuration) {
  return {
    /**
     *
     * @summary Evaluate images from mixed styles and return them in order
     * @param {EvaluateImagesBatch} body
     * @param {number} evaluatorId
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     */
    evaluatorEvaluatorIdEvaluatePost(
      body: EvaluateImagesBatch,
      evaluatorId: number,
      options?: any
    ): (fetch?: FetchAPI, basePath?: string) => Promise<Array<number>> {
      const localVarFetchArgs = EvaluatorApiFetchParamCreator(
        configuration
      ).evaluatorEvaluatorIdEvaluatePost(body, evaluatorId, options);
      return (
        fetch: FetchAPI = isomorphicFetch,
        basePath: string = BASE_PATH()
      ) => {
        return fetch(
          basePath + localVarFetchArgs.url,
          localVarFetchArgs.options
        ).then((response) => {
          if (response.status >= 200 && response.status < 300) {
            return response.json();
          } else {
            throw response;
          }
        });
      };
    },
    /**
     *
     * @summary Get the rating of a generated image
     * @param {number} evaluatorId
     * @param {string} style
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     */
    evaluatorEvaluatorIdEvaluateStyleGet(
      evaluatorId: number,
      style: string,
      options?: any
    ): (fetch?: FetchAPI, basePath?: string) => Promise<number> {
      const localVarFetchArgs = EvaluatorApiFetchParamCreator(
        configuration
      ).evaluatorEvaluatorIdEvaluateStyleGet(evaluatorId, style, options);
      return (
        fetch: FetchAPI = isomorphicFetch,
        basePath: string = BASE_PATH()
      ) => {
        return fetch(
          basePath + localVarFetchArgs.url,
          localVarFetchArgs.options
        ).then((response) => {
          if (response.status >= 200 && response.status < 300) {
            return response.json();
          } else {
            throw response;
          }
        });
      };
    },
  };
};

/**
 * EvaluatorApi - factory interface
 * @export
 */
export const EvaluatorApiFactory = function (
  configuration?: Configuration,
  fetch?: FetchAPI,
  basePath?: string
) {
  return {
    /**
     *
     * @summary Evaluate images from mixed styles and return them in order
     * @param {EvaluateImagesBatch} body
     * @param {number} evaluatorId
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     */
    evaluatorEvaluatorIdEvaluatePost(
      body: EvaluateImagesBatch,
      evaluatorId: number,
      options?: any
    ) {
      return EvaluatorApiFp(configuration).evaluatorEvaluatorIdEvaluatePost(
        body,
        evaluatorId,
        options
      )(fetch, basePath);
    },
    /**
     *
     * @summary Get the rating of a generated image
     * @param {number} evaluatorId
     * @param {string} style
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     */
    evaluatorEvaluatorIdEvaluateStyleGet(
      evaluatorId: number,
      style: string,
      options?: any
    ) {
      return EvaluatorApiFp(configuration).evaluatorEvaluatorIdEvaluateStyleGet(
        evaluatorId,
        style,
        options
      )(fetch, basePath);
    },
  };
};

/**
 * EvaluatorApi - object-oriented interface
 * @export
 * @class EvaluatorApi
 * @extends {BaseAPI}
 */
export class EvaluatorApi extends BaseAPI {
  /**
   *
   * @summary Evaluate images from mixed styles and return them in order
   * @param {EvaluateImagesBatch} body
   * @param {number} evaluatorId
   * @param {*} [options] Override http request option.
   * @throws {RequiredError}
   * @memberof EvaluatorApi
   */
  public evaluatorEvaluatorIdEvaluatePost(
    body: EvaluateImagesBatch,
    evaluatorId: number,
    options?: any
  ) {
    return EvaluatorApiFp(this.configuration).evaluatorEvaluatorIdEvaluatePost(
      body,
      evaluatorId,
      options
    )(this.fetch, this.basePath);
  }

  /**
   *
   * @summary Get the rating of a generated image
   * @param {number} evaluatorId
   * @param {string} style
   * @param {*} [options] Override http request option.
   * @throws {RequiredError}
   * @memberof EvaluatorApi
   */
  public evaluatorEvaluatorIdEvaluateStyleGet(
    evaluatorId: number,
    style: string,
    options?: any
  ) {
    return EvaluatorApiFp(
      this.configuration
    ).evaluatorEvaluatorIdEvaluateStyleGet(
      evaluatorId,
      style,
      options
    )(this.fetch, this.basePath);
  }
}
/**
 * GeneratorApi - fetch parameter creator
 * @export
 */
export const GeneratorApiFetchParamCreator = function (
  configuration?: Configuration
) {
  return {
    /**
     *
     * @summary Get an image generated by a mixed style
     * @param {string} style
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     */
    generatorGenerateStyleGet(style: string, options: any = {}): FetchArgs {
      // verify required parameter 'style' is not null or undefined
      if (style === null || style === undefined) {
        throw new RequiredError(
          "style",
          "Required parameter style was null or undefined when calling generatorGenerateStyleGet."
        );
      }
      const localVarPath = `/generator/generate/{style}`.replace(
        `{${"style"}}`,
        encodeURIComponent(String(style))
      );
      const localVarUrlObj = url.parse(localVarPath, true);
      const localVarRequestOptions = Object.assign({ method: "GET" }, options);
      const localVarHeaderParameter = {} as any;
      const localVarQueryParameter = {} as any;

      localVarUrlObj.query = Object.assign(
        {},
        localVarUrlObj.query,
        localVarQueryParameter,
        options.query
      );
      // fix override query string Detail: https://stackoverflow.com/a/7517673/1077943
      delete localVarUrlObj.search;
      localVarRequestOptions.headers = Object.assign(
        {},
        localVarHeaderParameter,
        options.headers
      );

      return {
        url: url.format(localVarUrlObj),
        options: localVarRequestOptions,
      };
    },
    /**
     *
     * @summary Generate new styles for a generator
     * @param {GeneratorSettings} body
     * @param {number} generatorId
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     */
    generatorGeneratorIdGenerateNewStylesPut(
      body: GeneratorSettings,
      generatorId: number,
      options: any = {}
    ): FetchArgs {
      // verify required parameter 'body' is not null or undefined
      if (body === null || body === undefined) {
        throw new RequiredError(
          "body",
          "Required parameter body was null or undefined when calling generatorGeneratorIdGenerateNewStylesPut."
        );
      }
      // verify required parameter 'generatorId' is not null or undefined
      if (generatorId === null || generatorId === undefined) {
        throw new RequiredError(
          "generatorId",
          "Required parameter generatorId was null or undefined when calling generatorGeneratorIdGenerateNewStylesPut."
        );
      }
      const localVarPath = `/generator/{generatorId}/generate-new-styles`.replace(
        `{${"generatorId"}}`,
        encodeURIComponent(String(generatorId))
      );
      const localVarUrlObj = url.parse(localVarPath, true);
      const localVarRequestOptions = Object.assign({ method: "PUT" }, options);
      const localVarHeaderParameter = {} as any;
      const localVarQueryParameter = {} as any;

      localVarHeaderParameter["Content-Type"] = "application/json";

      localVarUrlObj.query = Object.assign(
        {},
        localVarUrlObj.query,
        localVarQueryParameter,
        options.query
      );
      // fix override query string Detail: https://stackoverflow.com/a/7517673/1077943
      delete localVarUrlObj.search;
      localVarRequestOptions.headers = Object.assign(
        {},
        localVarHeaderParameter,
        options.headers
      );
      const needsSerialization =
        <any>"GeneratorSettings" !== "string" ||
        localVarRequestOptions.headers["Content-Type"] === "application/json";
      localVarRequestOptions.body = needsSerialization
        ? JSON.stringify(body || {})
        : body || "";

      return {
        url: url.format(localVarUrlObj),
        options: localVarRequestOptions,
      };
    },
    /**
     *
     * @summary Generate images from mixed styles and return them in order in a sprite map with the dimensions 1 x <number generated images>
     * @param {Array<StyleConfiguration>} body
     * @param {number} generatorId
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     */
    generatorGeneratorIdGeneratePost(
      body: Array<StyleConfiguration>,
      generatorId: number,
      options: any = {}
    ): FetchArgs {
      // verify required parameter 'body' is not null or undefined
      if (body === null || body === undefined) {
        throw new RequiredError(
          "body",
          "Required parameter body was null or undefined when calling generatorGeneratorIdGeneratePost."
        );
      }
      // verify required parameter 'generatorId' is not null or undefined
      if (generatorId === null || generatorId === undefined) {
        throw new RequiredError(
          "generatorId",
          "Required parameter generatorId was null or undefined when calling generatorGeneratorIdGeneratePost."
        );
      }
      const localVarPath = `/generator/{generatorId}/generate`.replace(
        `{${"generatorId"}}`,
        encodeURIComponent(String(generatorId))
      );
      const localVarUrlObj = url.parse(localVarPath, true);
      const localVarRequestOptions = Object.assign({ method: "POST" }, options);
      const localVarHeaderParameter = {} as any;
      const localVarQueryParameter = {} as any;

      localVarHeaderParameter["Content-Type"] = "application/json";

      localVarUrlObj.query = Object.assign(
        {},
        localVarUrlObj.query,
        localVarQueryParameter,
        options.query
      );
      // fix override query string Detail: https://stackoverflow.com/a/7517673/1077943
      delete localVarUrlObj.search;
      localVarRequestOptions.headers = Object.assign(
        {},
        localVarHeaderParameter,
        options.headers
      );
      const needsSerialization =
        <any>"Array&lt;StyleConfiguration&gt;" !== "string" ||
        localVarRequestOptions.headers["Content-Type"] === "application/json";
      localVarRequestOptions.body = needsSerialization
        ? JSON.stringify(body || {})
        : body || "";

      return {
        url: url.format(localVarUrlObj),
        options: localVarRequestOptions,
      };
    },
  };
};

/**
 * GeneratorApi - functional programming interface
 * @export
 */
export const GeneratorApiFp = function (configuration?: Configuration) {
  return {
    /**
     *
     * @summary Get an image generated by a mixed style
     * @param {string} style
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     */
    generatorGenerateStyleGet(
      style: string,
      options?: any
    ): (fetch?: FetchAPI, basePath?: string) => Promise<Blob> {
      const localVarFetchArgs = GeneratorApiFetchParamCreator(
        configuration
      ).generatorGenerateStyleGet(style, options);
      return (
        fetch: FetchAPI = isomorphicFetch,
        basePath: string = BASE_PATH()
      ) => {
        return fetch(
          basePath + localVarFetchArgs.url,
          localVarFetchArgs.options
        ).then((response) => {
          if (response.status >= 200 && response.status < 300) {
            return response.blob();
          } else {
            throw response;
          }
        });
      };
    },
    /**
     *
     * @summary Generate new styles for a generator
     * @param {GeneratorSettings} body
     * @param {number} generatorId
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     */
    generatorGeneratorIdGenerateNewStylesPut(
      body: GeneratorSettings,
      generatorId: number,
      options?: any
    ): (fetch?: FetchAPI, basePath?: string) => Promise<Response> {
      const localVarFetchArgs = GeneratorApiFetchParamCreator(
        configuration
      ).generatorGeneratorIdGenerateNewStylesPut(body, generatorId, options);
      return (
        fetch: FetchAPI = isomorphicFetch,
        basePath: string = BASE_PATH()
      ) => {
        return fetch(
          basePath + localVarFetchArgs.url,
          localVarFetchArgs.options
        ).then((response) => {
          if (response.status >= 200 && response.status < 300) {
            return response;
          } else {
            throw response;
          }
        });
      };
    },
    /**
     *
     * @summary Generate images from mixed styles and return them in order in a sprite map with the dimensions 1 x <number generated images>
     * @param {Array<StyleConfiguration>} body
     * @param {number} generatorId
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     */
    generatorGeneratorIdGeneratePost(
      body: Array<StyleConfiguration>,
      generatorId: number,
      options?: any
    ): (fetch?: FetchAPI, basePath?: string) => Promise<Blob> {
      const localVarFetchArgs = GeneratorApiFetchParamCreator(
        configuration
      ).generatorGeneratorIdGeneratePost(body, generatorId, options);
      return (
        fetch: FetchAPI = isomorphicFetch,
        basePath: string = BASE_PATH()
      ) => {
        return fetch(
          basePath + localVarFetchArgs.url,
          localVarFetchArgs.options
        ).then((response) => {
          if (response.status >= 200 && response.status < 300) {
            return response.blob();
          } else {
            throw response;
          }
        });
      };
    },
  };
};

/**
 * GeneratorApi - factory interface
 * @export
 */
export const GeneratorApiFactory = function (
  configuration?: Configuration,
  fetch?: FetchAPI,
  basePath?: string
) {
  return {
    /**
     *
     * @summary Get an image generated by a mixed style
     * @param {string} style
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     */
    generatorGenerateStyleGet(style: string, options?: any) {
      return GeneratorApiFp(configuration).generatorGenerateStyleGet(
        style,
        options
      )(fetch, basePath);
    },
    /**
     *
     * @summary Generate new styles for a generator
     * @param {GeneratorSettings} body
     * @param {number} generatorId
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     */
    generatorGeneratorIdGenerateNewStylesPut(
      body: GeneratorSettings,
      generatorId: number,
      options?: any
    ) {
      return GeneratorApiFp(
        configuration
      ).generatorGeneratorIdGenerateNewStylesPut(
        body,
        generatorId,
        options
      )(fetch, basePath);
    },
    /**
     *
     * @summary Generate images from mixed styles and return them in order in a sprite map with the dimensions 1 x <number generated images>
     * @param {Array<StyleConfiguration>} body
     * @param {number} generatorId
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     */
    generatorGeneratorIdGeneratePost(
      body: Array<StyleConfiguration>,
      generatorId: number,
      options?: any
    ) {
      return GeneratorApiFp(configuration).generatorGeneratorIdGeneratePost(
        body,
        generatorId,
        options
      )(fetch, basePath);
    },
  };
};

/**
 * GeneratorApi - object-oriented interface
 * @export
 * @class GeneratorApi
 * @extends {BaseAPI}
 */
export class GeneratorApi extends BaseAPI {
  /**
   *
   * @summary Get an image generated by a mixed style
   * @param {string} style
   * @param {*} [options] Override http request option.
   * @throws {RequiredError}
   * @memberof GeneratorApi
   */
  public generatorGenerateStyleGet(style: string, options?: any) {
    return GeneratorApiFp(this.configuration).generatorGenerateStyleGet(
      style,
      options
    )(this.fetch, this.basePath);
  }

  /**
   *
   * @summary Generate new styles for a generator
   * @param {GeneratorSettings} body
   * @param {number} generatorId
   * @param {*} [options] Override http request option.
   * @throws {RequiredError}
   * @memberof GeneratorApi
   */
  public generatorGeneratorIdGenerateNewStylesPut(
    body: GeneratorSettings,
    generatorId: number,
    options?: any
  ) {
    return GeneratorApiFp(
      this.configuration
    ).generatorGeneratorIdGenerateNewStylesPut(
      body,
      generatorId,
      options
    )(this.fetch, this.basePath);
  }

  /**
   *
   * @summary Generate images from mixed styles and return them in order in a sprite map with the dimensions 1 x <number generated images>
   * @param {Array<StyleConfiguration>} body
   * @param {number} generatorId
   * @param {*} [options] Override http request option.
   * @throws {RequiredError}
   * @memberof GeneratorApi
   */
  public generatorGeneratorIdGeneratePost(
    body: Array<StyleConfiguration>,
    generatorId: number,
    options?: any
  ) {
    return GeneratorApiFp(this.configuration).generatorGeneratorIdGeneratePost(
      body,
      generatorId,
      options
    )(this.fetch, this.basePath);
  }
}
/**
 * ModelsApi - fetch parameter creator
 * @export
 */
export const ModelsApiFetchParamCreator = function (
  configuration?: Configuration
) {
  return {
    /**
     *
     * @summary List all generators and evaluators + their settings
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     */
    modelsListGet(options: any = {}): FetchArgs {
      const localVarPath = `/models/list`;
      const localVarUrlObj = url.parse(localVarPath, true);
      const localVarRequestOptions = Object.assign({ method: "GET" }, options);
      const localVarHeaderParameter = {} as any;
      const localVarQueryParameter = {} as any;

      localVarUrlObj.query = Object.assign(
        {},
        localVarUrlObj.query,
        localVarQueryParameter,
        options.query
      );
      // fix override query string Detail: https://stackoverflow.com/a/7517673/1077943
      delete localVarUrlObj.search;
      localVarRequestOptions.headers = Object.assign(
        {},
        localVarHeaderParameter,
        options.headers
      );

      return {
        url: url.format(localVarUrlObj),
        options: localVarRequestOptions,
      };
    },
  };
};

/**
 * ModelsApi - functional programming interface
 * @export
 */
export const ModelsApiFp = function (configuration?: Configuration) {
  return {
    /**
     *
     * @summary List all generators and evaluators + their settings
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     */
    modelsListGet(
      options?: any
    ): (fetch?: FetchAPI, basePath?: string) => Promise<ModelsArray> {
      const localVarFetchArgs = ModelsApiFetchParamCreator(
        configuration
      ).modelsListGet(options);
      return (
        fetch: FetchAPI = isomorphicFetch,
        basePath: string = BASE_PATH()
      ) => {
        return fetch(
          basePath + localVarFetchArgs.url,
          localVarFetchArgs.options
        ).then((response) => {
          if (response.status >= 200 && response.status < 300) {
            return response.json();
          } else {
            throw response;
          }
        });
      };
    },
  };
};

/**
 * ModelsApi - factory interface
 * @export
 */
export const ModelsApiFactory = function (
  configuration?: Configuration,
  fetch?: FetchAPI,
  basePath?: string
) {
  return {
    /**
     *
     * @summary List all generators and evaluators + their settings
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     */
    modelsListGet(options?: any) {
      return ModelsApiFp(configuration).modelsListGet(options)(fetch, basePath);
    },
  };
};

/**
 * ModelsApi - object-oriented interface
 * @export
 * @class ModelsApi
 * @extends {BaseAPI}
 */
export class ModelsApi extends BaseAPI {
  /**
   *
   * @summary List all generators and evaluators + their settings
   * @param {*} [options] Override http request option.
   * @throws {RequiredError}
   * @memberof ModelsApi
   */
  public modelsListGet(options?: any) {
    return ModelsApiFp(this.configuration).modelsListGet(options)(
      this.fetch,
      this.basePath
    );
  }
}
