#Ejecutar en Azure Functions cuando se hace una petición HTTP


#Configurar function
import logging
import azure.functions as func
import openai

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:

#Hacer llamada a la API de OpenAI
        import os
        import openai
        openai.api_type = "azure"
        openai.api_base = "https://openai-sandbox-jep.openai.azure.com/"
        openai.api_version = "2022-12-01"
        openai.api_key = os.environ.get("OPENAI_API_KEY")

        response = openai.Completion.create(
            engine="davinci3",
            prompt=name,
            temperature=1,
            max_tokens=100,
            top_p=0.5,
            frequency_penalty=0,
            presence_penalty=0,
            best_of=1,
            stop=None)

        response = response['choices'][0]['text']

        return func.HttpResponse(f"{response}")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
