import socketserver
import re
import logging
import logging.config
import yaml

import settings

patttern = r'\d{4}\-\d{2}\-\d{2}\:\d{2}:\d{2}\.\d{3}\-\d{2}\r'
message_length = 1024

with open('log_conf.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)
logger = logging.getLogger('server_log')

class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            self.data = b''
            while True:
                message = self.request.recv(message_length)
                if not message:
                    break
                self.data += message
            result_code = self._parse_data()
            self.request.sendall(bytes(result_code))
        except Exception as e:
            logger.error(f'Exception occured: {e}')
            return 500

    def _parse_data(self):
        try:
            data = self.data.decode('utf-8')
            logger.info(f'Recieved data: {data}')
            messages = re.findall(patttern, data)

            if not messages:
                return 400

            for msg in messages:
                logger.info(f'Found pattern: {msg}')
                serialized_msg = msg.split('-')
                if serialized_msg[-1].strip() == '00':
                    with open(settings.output_file, 'a', encoding='utf-8') as fout:
                        partisipant_num, channel_id = serialized_msg[0], serialized_msg[1]
                        finish_time = serialized_msg[2][:len(serialized_msg[2]) - 2]
                        print(
                            f'Спортсмен, нагрудный номер {partisipant_num} прошёл отсечку {channel_id} в {finish_time}',
                            file=fout)
            return 200
        except Exception as e:
            logger.error(f'Exception occured: {e}')
            return 500


if __name__ == '__main__':
    with socketserver.TCPServer((settings.server_host, settings.server_port), TCPHandler) as server:
        print('server is running')
        server.serve_forever()