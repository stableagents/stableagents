import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class RouteConfig:
    route_id: str
    priority: int
    token_patterns: List[List[str]]  # List of token sequences that trigger this route
    confidence_threshold: float
    handler: callable

class NextTokenPredictor:
    def __init__(self, vocab_size: int, embedding_dim: int):
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        # Initialize with simple embedding matrix - in practice, this would be trained
        self.embedding_matrix = np.random.randn(vocab_size, embedding_dim)
        
    def predict_next_tokens(self, current_tokens: List[str], n_predictions: int = 5) -> List[Tuple[str, float]]:
        """
        Predict the next most likely tokens given the current sequence.
        Returns: List of (token, probability) tuples.
        """
        # Simplified prediction logic - would use proper language model in production
        token_embeddings = np.mean([self.embedding_matrix[hash(token) % self.vocab_size] 
                                  for token in current_tokens], axis=0)
        
        # Calculate similarities with all possible next tokens
        similarities = np.dot(self.embedding_matrix, token_embeddings)
        probabilities = np.exp(similarities) / np.sum(np.exp(similarities))
        
        # Get top N predictions
        top_indices = np.argsort(probabilities)[-n_predictions:]
        return [(f"token_{idx}", float(probabilities[idx])) for idx in top_indices]

class ResponseRouter:
    def __init__(self, predictor: NextTokenPredictor):
        self.predictor = predictor
        self.routes: List[RouteConfig] = []
        self.route_cache: Dict[str, List[RouteConfig]] = defaultdict(list)
        
    def add_route(self, route_config: RouteConfig):
        """Add a new routing configuration."""
        self.routes.append(route_config)
        # Sort routes by priority
        self.routes.sort(key=lambda x: x.priority, reverse=True)
        # Clear cache as routes have changed
        self.route_cache.clear()
        
    def _check_token_pattern(self, tokens: List[str], pattern: List[str]) -> float:
        """
        Check if token sequence matches pattern.
        Returns confidence score between 0 and 1.
        """
        if len(tokens) > len(pattern):
            return 0.0
            
        confidence = 1.0
        for actual, expected in zip(tokens, pattern):
            if actual != expected:
                confidence *= 0.5
        return confidence
    
    def _predict_pattern_match(self, 
                             tokens: List[str], 
                             pattern: List[str], 
                             depth: int = 3) -> float:
        """
        Predict likelihood of pattern matching based on next token predictions.
        """
        if len(tokens) >= len(pattern):
            return self._check_token_pattern(tokens, pattern)
            
        current_confidence = self._check_token_pattern(tokens, pattern[:len(tokens)])
        if current_confidence == 0:
            return 0
            
        next_token_predictions = self.predictor.predict_next_tokens(tokens)
        
        if depth == 0 or not next_token_predictions:
            return current_confidence
            
        # Recursive prediction for each possible next token
        max_future_confidence = max(
            self._predict_pattern_match(
                tokens + [pred[0]], 
                pattern,
                depth - 1
            ) * pred[1]
            for pred in next_token_predictions
        )
        
        return current_confidence * max_future_confidence

    def route_message(self, tokens: List[str]) -> Optional[callable]:
        """
        Route message based on current tokens and predicted next tokens.
        Returns appropriate handler function if route is found.
        """
        # Check cache first
        cache_key = " ".join(tokens)
        if cache_key in self.route_cache:
            matching_routes = self.route_cache[cache_key]
        else:
            matching_routes = []
            for route in self.routes:
                max_confidence = max(
                    self._predict_pattern_match(tokens, pattern)
                    for pattern in route.token_patterns
                )
                if max_confidence >= route.confidence_threshold:
                    matching_routes.append((max_confidence, route))
            
            # Sort by confidence * priority
            matching_routes.sort(
                key=lambda x: x[0] * x[1].priority, 
                reverse=True
            )
            matching_routes = [route for _, route in matching_routes]
            self.route_cache[cache_key] = matching_routes
        
        return matching_routes[0].handler if matching_routes else None

# Example usage
def create_demo_router() -> ResponseRouter:
    predictor = NextTokenPredictor(vocab_size=1000, embedding_dim=64)
    router = ResponseRouter(predictor)
    
    # Add some example routes
    router.add_route(RouteConfig(
        route_id="support",
        priority=10,
        token_patterns=[
            ["help", "needed"],
            ["support", "request"],
            ["issue", "with"]
        ],
        confidence_threshold=0.6,
        handler=lambda msg: "Routing to support team..."
    ))
    
    router.add_route(RouteConfig(
        route_id="sales",
        priority=5,
        token_patterns=[
            ["price", "quote"],
            ["purchase", "info"],
            ["buy", "product"]
        ],
        confidence_threshold=0.7,
        handler=lambda msg: "Routing to sales team..."
    ))
    
    return router