import pandas as pd

def find_lowest_cost_vm(memory_gb, vcpu_cores, os, pricesheet_df, rightsizing_df):
    filtered_df = rightsizing_df[(rightsizing_df['memoryInMB'] >= memory_gb * 1024) &
                                 (rightsizing_df['numberOfCores'] >= vcpu_cores) &
                                 (rightsizing_df['armSkuName'].isin(pricesheet_df['meterName'])) &
                                 (rightsizing_df['meterName'].isin(pricesheet_df['armSkuName'])) &
                                 (rightsizing_df['osDiskSizeInMB'] > 0) &
                                 (rightsizing_df['osDiskSizeInMB'] < float('inf')) &
                                 (rightsizing_df['meterName'].notnull()) &
                                 (rightsizing_df['armSkuName'].notnull()) &
                                 (rightsizing_df['osDiskSizeInMB'].notnull()) &
                                 (rightsizing_df['memoryInMB'].notnull())]

    if filtered_df.empty:
        return None

    joined_df = filtered_df.merge(pricesheet_df, left_on='meterName', right_on='armSkuName')

    joined_df['unitPricePerUnit'] = joined_df['unitPricePerUnit'].str.replace(',', '.').astype(float)

    lowest_cost_vm = joined_df.loc[joined_df['unitPricePerUnit'].idxmin()]

    return lowest_cost_vm


def main():
    # Loading CSV files
    print("Loading CSV files...")
    print("Pricesheet:")
    pricesheet_df = pd.read_csv('Exam Pricesheet.csv', delimiter=';')
    input()
    print("Rightsizing:")
    rightsizing_df = pd.read_csv('Exam rightsizing.csv', delimiter=';', header=1)
    rightsizing_df.columns = ['armSkuName', 'numberOfCores', 'osDiskSizeInMB', 'memoryInMB', 'maxDataDiskCount', 'meterName']
    vm1 = find_lowest_cost_vm(15, 4, 'Linux', pricesheet_df, rightsizing_df)
    if vm1 is not None:
        print("VM 1 - Linux:")
        print(vm1)

    vm2 = find_lowest_cost_vm(30, 2, 'Windows', pricesheet_df, rightsizing_df)
    if vm2 is not None:
        print("VM 2 - Windows:")
        print(vm2)

    vm3 = find_lowest_cost_vm(5, 1, 'Linux', pricesheet_df, rightsizing_df)
    if vm3 is not None:
        print("VM 3 - Linux:")
        print(vm3)

    vm4 = find_lowest_cost_vm(60, 6, 'Windows', pricesheet_df, rightsizing_df)
    if vm4 is not None:
        print("VM 4 - Windows:")
        print(vm4)



if __name__ == "__main__":
    main()