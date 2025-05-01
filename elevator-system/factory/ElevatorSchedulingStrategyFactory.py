from strategies.ShortestPathSchedulingStrategy import ShortestPathSchedulingStrategy
from strategies.LeastBusySchedulingStrategy import LeastBusySchedulingStrategy
from strategies.EnergyEfficientSchedulingStrategy import EnergyEfficientSchedulingStrategy

class ElevatorSchedulingStrategyFactory:
    @staticmethod
    def create_strategy(strategy_type="shortest_path"):
        """
        Create an elevator scheduling strategy based on the specified type.
        
        Args:
            strategy_type: The type of scheduling strategy to create ('shortest_path', 'least_busy', or 'energy_efficient')
            
        Returns:
            IElevatorSchedulingStrategy: An instance of the requested scheduling strategy
        """
        if strategy_type.lower() == "least_busy":
            return LeastBusySchedulingStrategy()
        elif strategy_type.lower() == "energy_efficient":
            return EnergyEfficientSchedulingStrategy()
        else:
            # Default to shortest path strategy
            return ShortestPathSchedulingStrategy()
