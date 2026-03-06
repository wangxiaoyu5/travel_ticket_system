from django.core.management.base import BaseCommand
from ticket.models import Region

class Command(BaseCommand):
    help = 'Update regions with province data'

    def handle(self, *args, **options):
        # 检查当前地区数据
        current_regions = Region.objects.all()
        self.stdout.write('Current regions:')
        for region in current_regions:
            self.stdout.write(f'- {region.name}')
        self.stdout.write(f'Total regions: {current_regions.count()}')

        # 定义省份列表
        provinces = [
            '北京市', '天津市', '河北省', '山西省', '内蒙古自治区',
            '辽宁省', '吉林省', '黑龙江省', '上海市', '江苏省',
            '浙江省', '安徽省', '福建省', '江西省', '山东省',
            '河南省', '湖北省', '湖南省', '广东省', '广西壮族自治区',
            '海南省', '重庆市', '四川省', '贵州省', '云南省',
            '西藏自治区', '陕西省', '甘肃省', '青海省', '宁夏回族自治区',
            '新疆维吾尔自治区', '香港特别行政区', '澳门特别行政区', '台湾省'
        ]

        # 添加缺失的省份
        added_count = 0
        for province in provinces:
            if not Region.objects.filter(name=province).exists():
                Region.objects.create(name=province)
                added_count += 1
                self.stdout.write(f'Added province: {province}')

        # 检查更新后的地区数据
        updated_regions = Region.objects.all()
        self.stdout.write(f'\nUpdated regions:')
        for region in updated_regions:
            self.stdout.write(f'- {region.name}')
        self.stdout.write(f'Total regions: {updated_regions.count()}')
        self.stdout.write(f'Added {added_count} provinces')
