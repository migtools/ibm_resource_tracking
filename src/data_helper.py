class DataHelper(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(DataHelper, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    vpc_infrastructure_data = {'VPCs': [], 'Subnets': [], 'Instances': [], 'Public Gateways': []}

    def get_vpc_infrastructure_data(self):
        print("Get", self.vpc_infrastructure_data)
        return self.vpc_infrastructure_data

    def set_vpc_infrastructure_data(self, vpc_infrastructure_data):
        self.vpc_infrastructure_data = vpc_infrastructure_data
        print(self.vpc_infrastructure_data)