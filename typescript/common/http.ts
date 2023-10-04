
import logger from "./logger";
import { ResponseError } from "./errors";

export const StatusCodes = {
    OK: 200,
    CREATED: 201,
} as const;
  

async function validateResponse(response: Response, expectedStatusCodes: number[], logResponses: boolean = false) {
    if (expectedStatusCodes.includes(response.status)) {
        if (logResponses) {
            logger.debug(`Received expected response (${response.status}) from ${response.url}`);
        }
    } else {
        const responseText = await response.text();
        throw new ResponseError(`Received unexpected response (${response.status}) from ${response.url}\n${responseText}`);
    }
}

export function HttpRequest(expectedStatusCodes: number[], logResponses: boolean = false) {
    return function (target: any, propertyKey: string, descriptor: PropertyDescriptor) { 
        const originalMethod = descriptor.value;

        descriptor.value = async function(...args: any[]): Promise<number> {
            let response: Response = await originalMethod.apply(this, args);
            await validateResponse(response, expectedStatusCodes, logResponses);
            return await response.json();
        }

        return descriptor;
    };
}
