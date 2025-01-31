from agents.walkietalkie.hallucination_predictor import create_hallucination_pipeline, process_text
from agents.walkietalkie.main import create_demo_router

def initialize_walkie_talkie():
    """Initialize and configure the walkie talkie components."""
    # Set up hallucination detection pipeline
    detector, validator, router = create_hallucination_pipeline()
    
    # Create response routing system
    response_router = create_demo_router()
    
    return {
        'hallucination_detector': detector,
        'hallucination_validator': validator, 
        'hallucination_router': router,
        'response_router': response_router
    }

