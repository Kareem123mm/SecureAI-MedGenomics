"""
Genetic Algorithm Security Optimizer

Optimizes security parameters using genetic algorithms
Based on research: "Advanced Security in Distributed Web Systems Using 
Genetic Algorithm-Based Techniques"
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
import logging
import random

logger = logging.getLogger(__name__)


class SecurityIndividual:
    """Represents an individual solution (security configuration)"""
    
    def __init__(self, parameters: Dict[str, float]):
        self.parameters = parameters
        self.fitness = 0.0
    
    def __repr__(self):
        return f"Individual(fitness={self.fitness:.3f}, params={self.parameters})"


class GeneticSecurityOptimizer:
    """
    Genetic Algorithm for optimizing security parameters
    
    Optimizes:
    - AML detection threshold
    - IDS sensitivity
    - Rate limiting values
    - Encryption strength
    """
    
    def __init__(
        self,
        population_size: int = 50,
        generations: int = 100,
        mutation_rate: float = 0.1,
        crossover_rate: float = 0.8
    ):
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        
        # Parameter bounds
        self.param_bounds = {
            "aml_threshold": (0.5, 0.99),
            "ids_sensitivity": (0.0, 1.0),
            "rate_limit": (10, 1000),
            "encryption_level": (0.5, 1.0)
        }
        
        self.population: List[SecurityIndividual] = []
        self.best_individual: Optional[SecurityIndividual] = None
        self.evolution_history: List[float] = []
        
        logger.info("Genetic Security Optimizer initialized")
    
    def _create_random_individual(self) -> SecurityIndividual:
        """Create random security configuration"""
        parameters = {}
        for param, (min_val, max_val) in self.param_bounds.items():
            parameters[param] = random.uniform(min_val, max_val)
        return SecurityIndividual(parameters)
    
    def _initialize_population(self):
        """Initialize random population"""
        self.population = [
            self._create_random_individual()
            for _ in range(self.population_size)
        ]
        logger.info(f"Initialized population of {self.population_size}")
    
    def _calculate_fitness(self, individual: SecurityIndividual) -> float:
        """
        Calculate fitness score for security configuration
        
        Fitness based on:
        - Security level (higher = better)
        - Performance impact (lower = better)
        - False positive rate (lower = better)
        """
        params = individual.parameters
        
        # Security score (0-100)
        security_score = (
            params["aml_threshold"] * 30 +
            params["ids_sensitivity"] * 30 +
            (params["encryption_level"] * 30) +
            (params["rate_limit"] / 1000) * 10
        )
        
        # Performance penalty (high rate limit = worse performance)
        performance_penalty = (params["rate_limit"] / 1000) * 5
        
        # False positive penalty (high sensitivity = more false positives)
        false_positive_penalty = params["ids_sensitivity"] * 5
        
        # Total fitness
        fitness = security_score - performance_penalty - false_positive_penalty
        
        return max(0, fitness)
    
    def _evaluate_population(self):
        """Evaluate fitness of entire population"""
        for individual in self.population:
            individual.fitness = self._calculate_fitness(individual)
        
        # Sort by fitness (descending)
        self.population.sort(key=lambda x: x.fitness, reverse=True)
        
        # Track best individual
        if self.best_individual is None or self.population[0].fitness > self.best_individual.fitness:
            self.best_individual = self.population[0]
    
    def _selection(self) -> Tuple[SecurityIndividual, SecurityIndividual]:
        """Tournament selection"""
        tournament_size = 5
        
        def tournament():
            contestants = random.sample(self.population, tournament_size)
            return max(contestants, key=lambda x: x.fitness)
        
        parent1 = tournament()
        parent2 = tournament()
        
        return parent1, parent2
    
    def _crossover(
        self,
        parent1: SecurityIndividual,
        parent2: SecurityIndividual
    ) -> Tuple[SecurityIndividual, SecurityIndividual]:
        """Single-point crossover"""
        if random.random() > self.crossover_rate:
            return parent1, parent2
        
        # Create children
        child1_params = {}
        child2_params = {}
        
        params = list(parent1.parameters.keys())
        crossover_point = random.randint(1, len(params) - 1)
        
        for i, param in enumerate(params):
            if i < crossover_point:
                child1_params[param] = parent1.parameters[param]
                child2_params[param] = parent2.parameters[param]
            else:
                child1_params[param] = parent2.parameters[param]
                child2_params[param] = parent1.parameters[param]
        
        child1 = SecurityIndividual(child1_params)
        child2 = SecurityIndividual(child2_params)
        
        return child1, child2
    
    def _mutate(self, individual: SecurityIndividual):
        """Gaussian mutation"""
        for param in individual.parameters:
            if random.random() < self.mutation_rate:
                min_val, max_val = self.param_bounds[param]
                
                # Add Gaussian noise
                noise = random.gauss(0, (max_val - min_val) * 0.1)
                new_value = individual.parameters[param] + noise
                
                # Clip to bounds
                individual.parameters[param] = max(min_val, min(max_val, new_value))
    
    def optimize(self) -> Dict[str, float]:
        """
        Run genetic algorithm optimization
        
        Returns:
            Optimized security parameters
        """
        logger.info("Starting genetic algorithm optimization...")
        
        # Initialize
        self._initialize_population()
        self._evaluate_population()
        
        # Evolution
        for generation in range(self.generations):
            new_population = []
            
            # Elitism: keep best 10%
            elite_size = self.population_size // 10
            new_population.extend(self.population[:elite_size])
            
            # Generate rest of population
            while len(new_population) < self.population_size:
                # Selection
                parent1, parent2 = self._selection()
                
                # Crossover
                child1, child2 = self._crossover(parent1, parent2)
                
                # Mutation
                self._mutate(child1)
                self._mutate(child2)
                
                new_population.extend([child1, child2])
            
            # Trim to population size
            self.population = new_population[:self.population_size]
            
            # Evaluate
            self._evaluate_population()
            
            # Track evolution
            self.evolution_history.append(self.best_individual.fitness)
            
            # Log progress
            if (generation + 1) % 10 == 0:
                logger.info(
                    f"Generation {generation + 1}/{self.generations}: "
                    f"Best fitness = {self.best_individual.fitness:.3f}"
                )
        
        logger.info(
            f"Optimization complete! Best fitness: {self.best_individual.fitness:.3f}"
        )
        
        return self.best_individual.parameters
    
    def get_evolution_history(self) -> List[float]:
        """Get fitness evolution over generations"""
        return self.evolution_history


if __name__ == "__main__":
    # Test
    optimizer = GeneticSecurityOptimizer(
        population_size=30,
        generations=50,
        mutation_rate=0.15,
        crossover_rate=0.8
    )
    
    best_params = optimizer.optimize()
    
    print("\n🧬 Optimization Results:")
    print("Best Parameters:")
    for param, value in best_params.items():
        print(f"  {param}: {value:.4f}")
    
    print(f"\nFinal Fitness: {optimizer.best_individual.fitness:.3f}")
