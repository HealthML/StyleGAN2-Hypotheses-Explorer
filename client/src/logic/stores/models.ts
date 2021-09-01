import { Evaluator, Generator, ModelsApi } from "../../api";
import { Writable } from "../tools/customStore";

let models: ReturnType<ModelsApi["modelsListGet"]> | undefined = undefined;
let generatorsWritable = new Writable<Generator[] | undefined>(undefined);
let evaluatorsWritable = new Writable<Evaluator[] | undefined>(undefined);

async function fetchModels() {
  if (!models) {
    models = new Promise(async (resolve) => {
      const models = await new ModelsApi().modelsListGet();
      generatorsWritable.set(models.generators);
      evaluatorsWritable.set(models.evaluators);
      resolve(models);
    });
  }
  await models;
}

export async function getEvaluators(): Promise<Writable<Evaluator[]>> {
  await fetchModels();
  return evaluatorsWritable as Writable<Evaluator[]>;
}

export async function getGenerators(): Promise<Writable<Generator[]>> {
  await fetchModels();
  return generatorsWritable as Writable<Generator[]>;
}
