import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def monty(selected_capacity, selected_items):

        max_capacity = selected_capacity
        items = selected_items

        #Prompt for number of simulations
        try:
                number_of_simulations = int(input("\nPlease enter number of simulations:" ))
                number_of_days =  int(input("\nPlease enter number of days to simulate (Suggested- 14 days):" ))

        except ValueError:
                print("Start over and please enter a INTEGER")


        #Arrays for simulation results
        daily_total_inventory = np.zeros((number_of_simulations, number_of_days))
        daily_total_demand = np.zeros((number_of_simulations, number_of_days))
        capacity_exceeded_days = np.zeros((number_of_simulations))


        # Generate simulations accoding to entered amount
        for simulation in range(number_of_simulations):
                print(f"running simulation {simulation + 1} out of {number_of_simulations}")

                #Generate days for each day that was entered
                for each_day in range(number_of_days):
                        inventory_levels= []
                        demand_levels= []

                        #Cycle through each item to generate inventory
                        for _, item in items.iterrows():

                                avg_inventory = item["avg_inventory"]
                                std_inventory = item["std_inventory"]
                                avg_demand = item["avg_demand"]
                                std_demand = item["std_demand"]

                                # Generate inventory and demand, no negative numbers
                                inventory = max(0, np.random.normal(avg_inventory,std_inventory))
                                demand = max(0, np.random.normal(avg_demand,std_demand))
                                remaining_inventory= max(0,inventory-demand)

                                inventory_levels.append(remaining_inventory)
                                demand_levels.append(demand)

                        #Calcualte total daily inventory- all items combined
                        total_daily_inventory = (sum(inventory_levels))
                        daily_total_inventory[simulation, each_day] = total_daily_inventory

                        total_daily_demand = sum(demand_levels)
                        daily_total_demand[simulation, each_day] = total_daily_demand
                        
                        #Check capacity
                        print(total_daily_inventory)
                        print(max_capacity)
                        if total_daily_inventory > max_capacity:
                                capacity_exceeded_days[simulation] += 1
        print(np.sum(capacity_exceeded_days))

        #Final simulation results fed to functions as a dictionary

        simulation_results = {
        "daily_total_inventory": daily_total_inventory,
        "daily_total_demand": total_daily_demand,
        "capacity_exceeded_days": capacity_exceeded_days,
        "item":item,
        "max_capacity":max_capacity,
        "Number_of_simulations": number_of_simulations,
        "Number_of_days" :number_of_days,
        }

        return(simulation_results)


def item_setup():

        items_set={
                "1":{"name" : "Small item set", "num_of_items" : 5500},
                "2":{"name" : "Medium item set ", "num_of_items": 10000},
                "3":{"name" : "Large item set", "num_of_items": 25500}
        }

        print("\nAvailable item sets:")

        for key,value in items_set.items():
                print(f'{key}: {value["name"]} has {value["num_of_items"]} items')

        while True:
                selected_item_set =input("\nSelect item set number : ")

                if selected_item_set in items_set:
                        num_of_items = items_set[selected_item_set]["num_of_items"]
                        items=list(range(num_of_items))

                    # Generate data for number of items entered
                        data= {
                            "Items" : items,
                            "avg_inventory": [max(0,np.random.normal(10,3)) for each_item in items],
                            "std_inventory": [max(0,np.random.normal(5,8)) for each_item in items],
                            "avg_demand":[max(0,np.random.normal(10,3)) for each_item in items],
                            "std_demand": [max(0,np.random.normal(5,8)) for each_item in items]}

                        #Add data to Dataframe
                        df = pd.DataFrame(data)

                        #Generate orginal list of tiem data, will be replaced by CSV upload
                        df.to_csv("Generated_Supply_and_Demand_Data.csv", index=False)
                        print("CSV file exported successfully.")

                        print("\n---- First five items only ---")
                        print(df.head())
                        return(df)

                else:
                    print("Not a valid entry, try again")


def warehouses_setup():

        # Max inventory of each WHSE must be replaced with real WHSE information. For now use generic capacities.

        warehouse={
                "1":{"name" : "Small Warehouse", "inventory_capacity" : 22000},
                "2":{"name" : "Medium Warehouse", "inventory_capacity": 40000},
                "3":{"name" : "Large Warehouse", "inventory_capacity": 102000}
                }

        print("\nAvailable warehouses:")

        for key,value in warehouse.items():
                print(f'{key}: {value["name"]} has capacity {value["inventory_capacity"]} ')

        while True:
                selected_warehouse =input("\nSelect warehouse number : ")

                if selected_warehouse in warehouse:
                        return warehouse[selected_warehouse]["inventory_capacity"]
                else:
                        print("Not a valid entry, try again")


def detailed_inventory_statistics(simulation_results):

        # Import dicitonay from monte and set local variables
        daily_inventory = simulation_results['daily_total_inventory']
        capacity_exceeded = simulation_results['capacity_exceeded_days']
        max_capacity = simulation_results['max_capacity']
        number_of_sims = simulation_results['Number_of_simulations']
        number_of_days = simulation_results['Number_of_days']

        # Create comprehensive statistics dataframe for daily inventory
        statistics = {
                # Inventory level statistics
                'Inventory Statistics': [
                'Mean Daily Inventory',
                'Median Daily Inventory',
                'Std Dev Daily Inventory',
                'Min Daily Inventory',
                'Max of Daily Inventory'
                ],
                'Value': [
                round(np.mean(daily_inventory),1),
                round(np.median(daily_inventory),1),
                round(np.std(daily_inventory),1),
                round(np.min(daily_inventory),1),
                round(np.max(daily_inventory),1),
                ]
                }

        # Create capacity exceeded sdataframe
        capacity_stats = {
                'Capacity Exceeded Statistics': [
                'Total Simulations Exceeding Capacity',
                'Mean Days Over Capacity per Simulation',
                'Max Days Over Capacity in a Simulation',
                        ],
                'Value': [
                round(np.sum(capacity_exceeded > 0),1),
                round(np.mean(capacity_exceeded),1),
                round(np.max(capacity_exceeded),1),
                        ]
                }

        # Capacity exceeded analysis
        # Days exceeded capacity analysis
        total_days_over_capacity_per_day = np.zeros(daily_inventory.shape[1])
        print( "\n Days over per simulaiton")

        for sim_index in range(daily_inventory.shape[0]):
                # Use original max capacity to determien number of days over
                days_over = daily_inventory[sim_index] >  max_capacity

                # Count days over capacity for this simulation
                days_over_capacity_per_sim= (f"Simulation {sim_index+1} had {np.sum(days_over)} days over WHSE max capacity ")
                print(days_over_capacity_per_sim)

                # Accumulate total days over capacity for each day across all simulations
                total_days_over_capacity_per_day += days_over

        print(f"\n Total simulations {number_of_sims}")

        # Days over capacity detailed analysis
        daily_over_capacity_stats = {
                'Daily Capacity Exceeded Details': [
                        'Days with Capacity Exceeded in Any Simulation',
                        'Max Simulations Exceeding Capacity on a Single Day',
                        'Percentage of Simulations Exceeding Capacity Daily'
                ],
                'Value': [
                        np.sum(total_days_over_capacity_per_day > 0),
                        np.max(total_days_over_capacity_per_day),
                        (np.sum(total_days_over_capacity_per_day > 0) / daily_inventory.shape[1]) * 100
                ]
                }


        # Create visualization of days over capacity
        plt.figure(figsize=(15, 6))
        plt.bar(range(len(total_days_over_capacity_per_day)), total_days_over_capacity_per_day)
        plt.title('Number of Simulations Exceeding Capacity per Day')
        plt.xlabel('Day')
        plt.ylabel('Number of Simulations Over Capacity')
        plt.tight_layout()
        plt.savefig('days_over_capacity.png')
        plt.close()

        # Print results
        print("\n--- Inventory Level Statistics ---")
        inventory_df = pd.DataFrame(statistics)
        print(inventory_df)

        print("\n--- Capacity Exceeded Statistics ---")
        capacity_df = pd.DataFrame(capacity_stats)
        print(capacity_df)

        print("\n--- Daily Capacity Exceeded Details ---")
        daily_df = pd.DataFrame(daily_over_capacity_stats)
        print(daily_df)



def visuals(simulation_results):

        #Boxplot of daily total inventory across simulations
        plt.figure(figsize=(15, 6))
        plt.boxplot(simulation_results['daily_total_inventory'])
        plt.title('Distribution of Daily Total Inventory Across Simulations')
        plt.xlabel('Simulation Run')
        plt.ylabel('Total Inventory Level')
        plt.tight_layout()
        plt.savefig('inventory_boxplot.png')
        plt.close()

        #Heatmap of daily inventory variation
        plt.figure(figsize=(15, 8))
        plt.imshow(simulation_results['daily_total_inventory'], cmap='YlGnBu')
        plt.title('Heatmap of Daily Total Inventory Levels')
        plt.xlabel('Days')
        plt.ylabel('Simulation Run')
        plt.tight_layout()
        plt.savefig('inventory_heatmap.png')
        plt.close()

        #Histogram of capacity exceeded days
        plt.figure(figsize=(10, 6))
        plt.hist(simulation_results['capacity_exceeded_days'], bins=10,
                         edgecolor='black')
        plt.title('Distribution of Days Exceeding Warehouse Capacity')
        plt.xlabel('Number of Days Over Capacity')
        plt.ylabel('Frequency')
        plt.tight_layout()
        plt.savefig('capacity_exceeded_histogram.png')
        plt.close()

    
        #Violin Plot of Daily Inventory Distribution
        plt.figure(figsize=(15, 6))
        plt.violinplot(simulation_results['daily_total_inventory'])
        plt.title('Violin Plot of Daily Total Inventory Distribution')
        plt.xlabel('Simulation Run')
        plt.ylabel('Total Inventory Level')
        plt.tight_layout()
        plt.savefig('inventory_violin.png')
        plt.close()


        # Stacked Area Chart of Inventory
        components = simulation_results['item']
        plt.figure(figsize=(15, 6))
        plt.stackplot(range(len(components)),
                components['avg_inventory'],
                components['avg_demand'],
                labels=['Average Inventory', 'Average Demand'])
        plt.title('Inventory')
        plt.xlabel('Item Index')
        plt.ylabel('Quantity')
        plt.legend(loc='upper right')
        plt.tight_layout()
        plt.savefig('inventory_components.png')
        plt.close()

def main():
        max_capacity = warehouses_setup()
        items = item_setup()
        simulation_results = monty(max_capacity, items)
        detailed_inventory_statistics(simulation_results)
        visuals(simulation_results)

main()
