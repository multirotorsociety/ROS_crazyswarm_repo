import csv
import yaml

csv_filename = 'formation_positions_ccw.csv'
output_filename = 'allCrazyflies.yaml'
formation = 2
# 1: big 5m circle
# 2: double 5m and 3m circle

x = []
y = []
id = []

def main(csv_filename,output_filename):
    # reading csv file
    with open(csv_filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        if formation == 1:
            column = 0
        elif formation == 2:
            column = 9
        else:
            raise ValueError('Invalid formation number')
        line_count = 0
        for row in csv_reader:
            if line_count >= 2:     # skip header rows
                # print(int(row[column]))
                
                id.append(int(row[column]))
                x.append(float(row[column+6]))
                y.append(float(row[column+7]))
            line_count += 1

    # creating list of crazyflies
    cf_list = []
    for i in range(len(x)):
        cf_dict = {}
        cf_dict['id'] = id[i]
        cf_dict['channel'] = 20 + 10 * ((id[i]-1)//5)
        cf_dict['initialPosition'] = [x[i],y[i],0.0]
        cf_dict['type'] = 'default'
        cf_list.append(cf_dict)

    yaml_dict = {'crazyflies': cf_list}
    #print(yaml_dict)

    # writing to yaml file
    with open(output_filename,'w') as yaml_file:
        yaml.dump(yaml_dict, yaml_file, sort_keys=False)

    print("\n Done writing yaml file.")


if __name__ == "__main__":
    main(csv_filename,output_filename)