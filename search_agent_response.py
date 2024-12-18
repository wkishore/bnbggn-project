from google.api_core.client_options import ClientOptions
from google.cloud import discoveryengine_v1 as discoveryengine
from extracting_info import extract_info_from_search_results
import vertexai
from vertexai.generative_models import GenerativeModel
from dotenv import load_dotenv
import os

load_dotenv()

project_id = os.getenv("PROJECT_ID")
location = os.getenv("LOCATION") 
engine_id = os.getenv("ENGINE_ID")

def answer_query_sample(
    preamble:str,
    prompt:str,
    project_id: str = project_id,
    location: str =  location,
    engine_id: str = engine_id,
) -> discoveryengine.AnswerQueryResponse:
    
    client_options = (
        ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
        if location != "global"
        else None
    )

    client = discoveryengine.ConversationalSearchServiceClient(
        client_options=client_options
    )

    serving_config = f"projects/{project_id}/locations/{location}/collections/default_collection/engines/{engine_id}/servingConfigs/default_serving_config"

    query_understanding_spec = discoveryengine.AnswerQueryRequest.QueryUnderstandingSpec(
        query_rephraser_spec=discoveryengine.AnswerQueryRequest.QueryUnderstandingSpec.QueryRephraserSpec(
            disable=True,  # Optional: Disable query rephraser
            max_rephrase_steps=3,  # Optional: Number of rephrase steps
        ),
        # Optional: Classify query types
        query_classification_spec=discoveryengine.AnswerQueryRequest.QueryUnderstandingSpec.QueryClassificationSpec(
            types=[
                discoveryengine.AnswerQueryRequest.QueryUnderstandingSpec.QueryClassificationSpec.Type.ADVERSARIAL_QUERY,
                discoveryengine.AnswerQueryRequest.QueryUnderstandingSpec.QueryClassificationSpec.Type.NON_ANSWER_SEEKING_QUERY,
            ]  # Options: ADVERSARIAL_QUERY, NON_ANSWER_SEEKING_QUERY or both
        ),
    )

    answer_generation_spec = discoveryengine.AnswerQueryRequest.AnswerGenerationSpec(
        ignore_adversarial_query=False,  # Optional: Ignore adversarial query
        ignore_non_answer_seeking_query=False,  # Optional: Ignore non-answer seeking query
        ignore_low_relevant_content=False,  # Optional: Return fallback answer when content is not relevant
        model_spec=discoveryengine.AnswerQueryRequest.AnswerGenerationSpec.ModelSpec(
            model_version="gemini-1.5-flash-001/answer_gen/v2",  # Optional: Model to use for answer generation
        ),
        prompt_spec=discoveryengine.AnswerQueryRequest.AnswerGenerationSpec.PromptSpec(
            preamble=preamble,  # Optional: Natural language instructions for customizing the answer.
        ),
        include_citations=True,  
        answer_language_code="en",  
    )

    # Initialize request argument(s)
    request = discoveryengine.AnswerQueryRequest(
        serving_config=serving_config,
        query=discoveryengine.Query(text=prompt),
        session=None,  
        query_understanding_spec=query_understanding_spec,
        answer_generation_spec=answer_generation_spec,
    )

    response = client.answer_query(request)
    
    extracted = extract_info_from_search_results(response.answer.steps[0].actions[0].observation.search_results)
    
    vertexai.init(project=project_id)

    model = GenerativeModel("gemini-2.0-flash-exp")

    prompt=preamble+extracted[:min(1000,len(extracted)//2)]+prompt+" Give response in Hindi "+"Keep it breif"
    
    print(prompt)


    response = model.generate_content(prompt)
    #print(response)
    return response.text
    return response.answer.answer_text

