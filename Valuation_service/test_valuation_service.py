import unittest
from product import Product
from input_output_handler import IoManager

class ValuationServiceTest(unittest.TestCase):
    def setUp(self):
        self.currencies_file = 'Test_dataset/test_currencies.csv'
        self.matchings_file = 'Test_dataset/test_matching.csv'
        self.data_file = 'Test_dataset/test_data.csv'
        self.top_products_file = 'Test_dataset/test_top_products.csv'

    def test_valuation_service(self):
        currencies_reader = IoManager(self.currencies_file)
        currencies_reader.read()
        currencies_dict = currencies_reader.getDict()

        matchings_reader = IoManager(self.matchings_file)
        matchings_reader.read()
        matchings_dict = matchings_reader.getDict()

        data_reader = IoManager(self.data_file)
        data_reader.read()

        product_list = []
        for line in data_reader.lines:
            l = line.strip().split(',')
            if len(l) == 5:
                product_list.append(Product(l[0], l[1], l[2], l[3], l[4], currencies_dict))

        product_group = {}
        for p in product_list:
            if p.matching_id in product_group.keys():
                pl = product_group[p.matching_id]
                pl.append(p)
            else:
                product_group[p.matching_id] = [p]

        output_lines = ['matching_id,total_price,avg_price,currency,ignored_products_count\n']
        for i in product_group:
            htp = max([p.total_price for p in product_group[i]])
            ap = sum([p.total_price for p in product_group[i]]) / len(product_group[i])
            output_lines.append(f'{i},{htp},{ap},{product_group[i][0].currency},0\n')

        top_product_writer = IoManager(self.top_products_file)
        top_product_writer.write(output_lines)

        # Perform assertions to validate the output
        expected_output = [
            'matching_id,total_price,avg_price,currency,ignored_products_count\n',
            '1,48000.0,48000.0,PLN,0\n',
            '3,2470.0,2470.0,PLN,0\n',
            '2,5060.0,3730.0,PLN,0\n',
        ]

        with open(self.top_products_file, 'r') as f:
            actual_output = f.readlines()

        self.assertEqual(expected_output, actual_output)

if __name__ == '__main__':
    unittest.main()
