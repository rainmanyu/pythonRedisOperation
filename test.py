from decimal import Decimal

import jsonUtil
import logging

# logging.basicConfig(filename='run.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
# jsonUtil.update_versions()

print(Decimal('5.000').quantize(Decimal('0.00')))
