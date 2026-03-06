from django.core.management.base import BaseCommand
from ticket.models import ScenicSpot

class Command(BaseCommand):
    help = 'Clean tags by removing category-related tags'

    def handle(self, *args, **options):
        # 定义需要移除的标签列表
        tags_to_remove = [
            '主题乐园类', '休闲度假类', '自然风光类', '历史文化类',
            '农业乡村类', '历史遗迹类', '民俗文化类', '宗教文化类',
            '现代都市类', '主题乐园', '休闲度假', '自然风光',
            '历史文化', '农业乡村', '历史遗迹', '民俗文化',
            '宗教文化', '现代都市'
        ]

        # 获取所有景点
        scenic_spots = ScenicSpot.objects.all()
        updated_count = 0

        for spot in scenic_spots:
            if spot.tags:
                # 分割标签为列表
                tag_list = [tag.strip() for tag in spot.tags.split(',') if tag.strip()]
                # 过滤掉需要移除的标签
                filtered_tags = [tag for tag in tag_list if tag not in tags_to_remove]
                # 如果标签有变化，更新景点
                if len(filtered_tags) != len(tag_list):
                    spot.tags = ','.join(filtered_tags) if filtered_tags else ''
                    spot.save()
                    updated_count += 1
                    self.stdout.write(f'Updated tags for {spot.name}: {spot.tags}')

        self.stdout.write(f'\nUpdated {updated_count} scenic spots')
        self.stdout.write('Tag cleaning completed')
