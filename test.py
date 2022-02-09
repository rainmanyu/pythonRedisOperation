import jsonUtil
import logging

logging.basicConfig(filename='run.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
jsonUtil.update_versions()
