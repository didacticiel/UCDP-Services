from typing import Optional


class Request(dict):

    def get_ip(self) -> Optional[str]:
        try:
            forwarded_id = self['headers']['x-forwarded-for']

            if ',' not in forwarded_id:
                return forwarded_id

            all_ips = forwarded_id.split(',')
            return all_ips[0]  # First IP should be correct, other ips could be vpns or cloudflare
        except Exception:
            return None

    def get_origin(self) -> str:
        return self.get('headers', {}).get('origin', '')
