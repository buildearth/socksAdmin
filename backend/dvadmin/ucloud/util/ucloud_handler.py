

class UcloudHandler:
    def __init__(self, region_code, public_key, signature, project_id):
        self.region_code = region_code
        self.public_key = public_key
        self.signature = signature
        self.project_id = project_id

        self.common_params = {
            'Region': self.region_code,
            "PublicKey": self.public_key,
            "Signature": self.signature,
            "ProjectId": self.project_id,
        }

    @staticmethod
    def get_all_resource_type(self):
        data = {
            "虚拟网卡": "uni",
            "云主机": "uhost",
        }
        return data


class EIPHandler(UcloudHandler):
    def __init__(self, region, public_key, signature, project_id, resource_type, resource_id,):
        super().__init__(region, public_key, signature, project_id)
        self.resource_type = resource_type
        self.resource_id = resource_id

    def unbind_eip(self, eip_id):
        url = 'https://api.ucloud.cn/?Action=UnBindEIP'
        params = {
            'EIPId': eip_id,
            'ResourceType': self.resource_type,
            'ResourceId': self.resource_id
        }
        params.update(self.common_params)

    def bind_eip(self, eip_id, private_ip):
        url = 'https://api.ucloud.cn/?Action=BindEIP'
        params = {
            'EIPId': eip_id,
            'ResourceType': self.resource_type,
            'ResourceId': self.resource_id
        }
        params.update(self.common_params)
        if self.resource_type == 'uni':
            params['PrivateIP'] = private_ip

    def release_eip(self, eip_id):
        url = 'https://api.ucloud.cn/?Action=ReleaseEIP'
        params = {
            'EIPId': eip_id,
        }
        params.update(self.common_params)

    def allocate_eip(self):
        url = 'https://api.ucloud.cn/?Action=AllocateEIP'


