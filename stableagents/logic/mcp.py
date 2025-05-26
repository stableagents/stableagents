import tensorflow as tf
import numpy as np
from typing import List, Dict, Any, Optional

class MCP:
    """Model-Controller-Predictor (MCP) implementation for stable AI agents."""
    
    def __init__(self, 
                 model: tf.keras.Model,
                 controller: tf.keras.Model,
                 predictor: tf.keras.Model,
                 config: Dict[str, Any]):
        """
        Initialize MCP components.
        
        Args:
            model: Main neural network model
            controller: Controller network for action selection
            predictor: Predictor network for state prediction
            config: Configuration dictionary
        """
        self.model = model
        self.controller = controller
        self.predictor = predictor
        self.config = config
        
        # Initialize optimizer
        self.optimizer = tf.keras.optimizers.Adam(
            learning_rate=config.get('learning_rate', 0.001)
        )
        
    def predict(self, state: np.ndarray) -> np.ndarray:
        """
        Generate predictions for the next state.
        
        Args:
            state: Current state observation
            
        Returns:
            Predicted next state
        """
        return self.predictor.predict(state, verbose=0)
    
    def control(self, state: np.ndarray) -> np.ndarray:
        """
        Generate control actions based on current state.
        
        Args:
            state: Current state observation
            
        Returns:
            Control actions
        """
        return self.controller.predict(state, verbose=0)
    
    def update(self, 
              states: np.ndarray,
              actions: np.ndarray,
              rewards: np.ndarray,
              next_states: np.ndarray) -> Dict[str, float]:
        """
        Update all networks using collected experience.
        
        Args:
            states: Batch of states
            actions: Batch of actions
            rewards: Batch of rewards
            next_states: Batch of next states
            
        Returns:
            Dictionary of loss values
        """
        with tf.GradientTape() as tape:
            # Model loss
            model_pred = self.model([states, actions])
            model_loss = tf.reduce_mean(
                tf.square(next_states - model_pred)
            )
            
            # Controller loss
            ctrl_pred = self.controller(states)
            ctrl_loss = -tf.reduce_mean(rewards)
            
            # Predictor loss
            pred_next = self.predictor(states)
            pred_loss = tf.reduce_mean(
                tf.square(next_states - pred_next)
            )
            
            # Total loss
            total_loss = model_loss + ctrl_loss + pred_loss
            
        # Apply gradients
        grads = tape.gradient(total_loss, 
                            self.model.trainable_variables + 
                            self.controller.trainable_variables +
                            self.predictor.trainable_variables)
        self.optimizer.apply_gradients(
            zip(grads, 
                self.model.trainable_variables + 
                self.controller.trainable_variables +
                self.predictor.trainable_variables)
        )
        
        return {
            'model_loss': float(model_loss),
            'controller_loss': float(ctrl_loss),
            'predictor_loss': float(pred_loss),
            'total_loss': float(total_loss)
        }
