from env import MicroEnv
import requests

class CDN:
    @staticmethod
    def upload_file(file, title: str, detail: str, level: int = 0) -> str:
        res = requests.post(
            f'http://{MicroEnv.CDN}/internal/cdn/upload',
            files={
                'file': file,
            },
            data={
                'title': title,
                'detail': detail,
                'level': level
            }
        )

        if res.status_code == 200:
            return res.content.decode('utf-8')
        else:
            raise Exception(res.status_code)