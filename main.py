import pandas as pd
def find_lowest_cost_vm(memory_gb, vcpu_cores, os, pricesheet_df, rightsizing_df):
    # Filter the pricesheet_df DataFrame based on the os value
    filtered_pricesheet_df = pricesheet_df[pricesheet_df['os'] == os]
    
    # Filter the rightsizing_df DataFrame based on the memory_gb, vcpu_cores, and filtered_pricesheet_df DataFrames
    filtered_df = rightsizing_df[(rightsizing_df['memoryInMB'] >= memory_gb * 1024) &
                                 (rightsizing_df['numberOfCores'] >= vcpu_cores) &
                                 (rightsizing_df['armSkuName'].isin(filtered_pricesheet_df['armSkuName'])) &
                                 (rightsizing_df['meterName'].isin(filtered_pricesheet_df['meterName']))]
    
    # Merge the filtered_df and filtered_pricesheet_df DataFrames based on the meterName column
    joined_df = filtered_df.merge(filtered_pricesheet_df, left_on='meterName', right_on='meterName')

    # Replace commas with periods in the unitPricePerUnit column and convert it to a float data type
    joined_df['unitPricePerUnit'] = joined_df['unitPricePerUnit'].str.replace(',', '.').astype(float)

    # Check if the joined_df DataFrame is empty and return None if it is
    if joined_df.empty:
        return None

    # Find the row in the joined_df DataFrame with the lowest unitPricePerUnit value
    lowest_cost_vm = joined_df.loc[joined_df['unitPricePerUnit'].idxmin()]

    # Return the row with the lowest unitPricePerUnit value
    return lowest_cost_vm



def main():
    print("Loading CSV files...")
    print("Pricesheet:")
    pricesheet_df = pd.read_csv('Exam Pricesheet.csv', delimiter=';')
    print("Rightsizing:")
    rightsizing_df = pd.read_csv('Exam rightsizing.csv', delimiter=';', header=1)
    rightsizing_df.columns = ['armSkuName', 'numberOfCores', 'osDiskSizeInMB', 'memoryInMB', 'maxDataDiskCount', 'meterName']
    vm1 = find_lowest_cost_vm(15, 4, 'Linux', pricesheet_df, rightsizing_df)
    if vm1 is not None:
        print("VM 1 - Linux:")
        print(vm1)

    vm2 = find_lowest_cost_vm(30, 2,'Windows', pricesheet_df, rightsizing_df)
    if vm2 is not None:
        print("VM 2 - Windows:")
        print(vm2)

    vm3 = find_lowest_cost_vm(5, 1,'Linux', pricesheet_df, rightsizing_df)
    if vm3 is not None:
        print("VM 3 - Linux:")
        print(vm3)

    vm4 = find_lowest_cost_vm(60, 6,'Windows', pricesheet_df, rightsizing_df)
    if vm4 is not None:
        print("VM 4 - Windows:")
        print(vm4)



if __name__ == "__main__":
    main()