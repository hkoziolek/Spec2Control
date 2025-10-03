# Standard library imports
import os
import re
import uuid
from typing import Dict, List, Optional, Union

# Third-party imports
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from openai import AsyncAzureOpenAI
from pydantic import BaseModel, field_validator

# PyMuPDF import with error handling
try:
    import fitz  # PyMuPDF
    # Verify that this is the correct PyMuPDF fitz module
    if not hasattr(fitz, 'open'):
        raise ImportError("The installed 'fitz' module is not PyMuPDF. Please uninstall any conflicting 'fitz' packages and install PyMuPDF.")
except ImportError:
    print("Error: PyMuPDF not installed or wrong 'fitz' package detected.")
    print("Please run: pip uninstall fitz && pip install PyMuPDF")
    raise

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define proper message types
from openai.types.chat import ChatCompletionMessageParam

conversations: Dict[str, List[ChatCompletionMessageParam]] = {}

def normalize_content_whitespace(content: str) -> str:
    """
    Normalize whitespace in content for diagram processing.
    Handles markdown code blocks and escaped newlines.
    
    Args:
        content: Raw content string
        
    Returns:
        Normalized content string
    """
    if not content:
        return content
    
    # Remove markdown code block formatting if present
    # Handle cases like ```json\n{...}\n``` or ```\n{...}\n```
    content = re.sub(r'^```(?:json)?\s*\n', '', content.strip())
    content = re.sub(r'\n```\s*$', '', content)
    
    # Convert literal \n sequences to actual newlines
    content = content.replace('\\n', '\n')
    
    # Convert literal \t sequences to actual tabs
    content = content.replace('\\t', '\t')
    
    # Replace multiple consecutive newlines with double newlines
    # This handles \n\n\n, \n\n\n\n, etc.
    normalized = re.sub(r'\n{3,}', '\n\n', content)
    
    # Remove trailing whitespace from each line
    lines = normalized.split('\n')
    lines = [line.rstrip() for line in lines]
    
    # Remove excessive leading/trailing newlines
    normalized = '\n'.join(lines).strip()
    
    return normalized

def get_llm_client(endpoint: Optional[str] = None, api_key: Optional[str] = None, api_version: Optional[str] = None):
    return AsyncAzureOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version=api_version
    )

async def llm_token_stream(messages: List[ChatCompletionMessageParam], 
                           llm_model: Optional[str] = None, 
                           temperature: Optional[float] = None, 
                           max_tokens: Optional[int] = None,
                           client: Optional[AsyncAzureOpenAI] = None, 
                           deployment_name: Optional[str] = None):
    """Async generator with full conversation history and configurable parameters."""
    # Use provided client or default
    active_client = client
    
    # Use deployment name if provided, otherwise map from model
    if deployment_name:
        model_name = deployment_name
    else:
        model_name = "gpt-5"
    
    temp = temperature if temperature is not None else 0.0
    tokens = max_tokens or 20000
    
    stream = await active_client.chat.completions.create(
        model=model_name,
        messages=messages,  # Now properly typed
        temperature=temp,
        #max_tokens=tokens,
        max_completion_tokens=tokens,
        stream=True
    )
    async for chunk in stream:
        # Check if chunk has choices and the first choice exists
        if chunk.choices and len(chunk.choices) > 0:
            delta = chunk.choices[0].delta
            if delta.content:
                yield delta.content

@app.post("/qa")
async def qa(req: Request):
    print("Received request for /qa endpoint")
    try:
        body = await req.json()
        session_id = body.get("session_id", str(uuid.uuid4()))
        user_message = body["prompt"]

        # Extract LLM settings from request
        llm_model = body.get("llmModel")
        temperature = body.get("temperature")
        max_tokens = body.get("maxTokens")
        
        # Extract custom API settings
        endpoint = body.get("endpoint")
        api_key = body.get("apiKey")
        api_version = body.get("apiVersion")
        deployment_name = body.get("deploymentName")
        
        # Get appropriate client
        custom_client = None
        if endpoint and api_key:
            custom_client = get_llm_client(endpoint, api_key, api_version)

        # Validate message is not empty
        if not user_message or not user_message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")

        # Initialize or get existing conversation
        if session_id not in conversations:
            conversations[session_id] = []        # Add user message to history with proper typing
        conversations[session_id].append({
            "role": "user", 
            "content": user_message
        })
        
        async def response_generator():
            response_token_count = 0
            
            # Estimate input tokens (rough approximation: 1 token ≈ 4 characters)
            input_text = ""
            for msg in conversations[session_id]:
                input_text += f"{msg['role']}: {msg['content']} "
            input_token_estimate = len(input_text) // 4
            print(f"Estimated tokens sent TO LLM: ~{input_token_estimate}")
            
            try:
                async for token in llm_token_stream(
                    conversations[session_id], 
                    llm_model=llm_model, 
                    temperature=temperature, 
                    max_tokens=max_tokens,
                    client=custom_client,
                    deployment_name=deployment_name
                ):
                    response_token_count += 1
                    yield token
            finally:
                print(f"Tokens received FROM LLM: {response_token_count}")
                # Clear conversation after streaming to make the endpoint stateless
                if session_id in conversations:
                    del conversations[session_id]
                
        return StreamingResponse(
            response_generator(),
            media_type="text/plain"
        )
    except Exception as e:
        print(f"Error in qa endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


class TransferOpenPLCRequest(BaseModel):
    project: str
    application: str
    diagram: str  # Optional for OpenPLC, will be ignored by backend
    content: str
    exportPath: str

    @field_validator('project', 'application')
    @classmethod
    def validate_non_empty_strings(cls, v):
        if not v or not v.strip():
            raise ValueError('Field cannot be empty or whitespace only')
        return v.strip()

    @field_validator('diagram')
    @classmethod
    def validate_diagram_optional(cls, v):
        # Diagram field is optional for OpenPLC - allow empty values
        if v is None:
            return ""
        return v.strip()

    @field_validator('exportPath')
    @classmethod
    def validate_export_path(cls, v):
        if not v or not v.strip():
            raise ValueError('Export path cannot be empty or whitespace only')
        return v.strip()

    @field_validator('content')
    @classmethod
    def validate_content(cls, v):
        if not v or not v.strip():
            raise ValueError('Content cannot be empty or whitespace only')

        # Check content size (limit to 1MB)
        if len(v.encode('utf-8')) > 1024 * 1024:
            raise ValueError('Content size cannot exceed 1MB')

        return v

# Pydantic models for function execution
class FunctionExecuteRequest(BaseModel):
    function_name: str
    parameters: Dict[str, Union[str, int, float, bool]]

class FunctionMetadataResponse(BaseModel):
    name: str
    description: str
    parameters: List[Dict[str, Union[str, bool]]]
    return_type: str
    return_description: str

@app.post("/transfer-openplc")
async def transfer_openplc(request: TransferOpenPLCRequest):
    """Transfer diagram to OpenPLC using project, application, exportPath, and content parameters. The diagram field is ignored for OpenPLC exports."""
    try:
        print(f"Processing OpenPLC export request for project: {request.project}, application: {request.application}")
        print(f"Export path: {request.exportPath}")
        if request.diagram:
            print(f"Note: Diagram field '{request.diagram}' is ignored for OpenPLC exports")
        else:
            print("Note: Diagram field is empty (as expected for OpenPLC exports)")
        
        # Normalize content whitespace (reuse existing function)
        normalized_content = normalize_content_whitespace(request.content)
        content_type = "Function Diagram"
        print(f"Detected content type: {content_type}")
    
        # Import the export function
        from export_openplc import export_to_openplc
        
        # Call the OpenPLC export function
        print("Calling OpenPLC export functionality...")
        export_result = export_to_openplc(
            project=request.project,
            application=request.application,
            export_path=request.exportPath,
            content=normalized_content
        )
        
        if not export_result.get("success", False):
            # Export failed, return error response
            error_msg = export_result.get("error", "Unknown export error")
            raise HTTPException(
                status_code=500,
                detail=f"OpenPLC export failed: {error_msg}"
            )
        
        # Return success response with detailed information from export
        return {
            "message": export_result.get("message", "OpenPLC Export completed"),
            "project": request.project,
            "application": request.application,
            "diagram": request.diagram if request.diagram else "(ignored for OpenPLC)",
            "exportPath": request.exportPath,
            "content_type": content_type,
            "content_size_bytes": len(request.content.encode('utf-8')),
            "normalized_content_size_bytes": len(normalized_content.encode('utf-8')),
            "validation_passed": True,
            "export_details": export_result,
            "note": "Diagram field is ignored for OpenPLC exports"
        }
        
    except HTTPException:
        # Re-raise HTTPException as-is (these are our specific error messages)
        raise
    except Exception as e:
        # Catch any other unexpected errors
        print(f"Unexpected error in transfer_openplc: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error during OpenPLC export: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    print("Starting Spec2Control Backend API...")
    print("Server will run on http://127.0.0.1:8001")
    print("Press Ctrl+C to stop")
    print("-" * 60)
    uvicorn.run(app, host="127.0.0.1", port=8001, reload=True)
